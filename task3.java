import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.util.concurrent.CountDownLatch;

/**
 * Task 3 - Cache Line Contention (False Sharing).
 *
 * Each of N threads increments its own slot 50,000,000 times:
 *   1. Unpadded : slots are adjacent in one long[] -> threads share cache lines
 *   2. Padded   : slots are 128 bytes apart        -> one cache line per thread
 *   3. Local    : thread keeps a local variable, writes the slot once at the end
 *
 * Usage:  java Task3.java [threads]
 * Default threads = availableProcessors(). Pass your PHYSICAL core count
 * as the argument if it differs (e.g. hyper-threading machines).
 */
public class Task3 {
    static final String STUDENT_ID = "230103129";
    static final long ITERATIONS = 50_000_000L;
    static final int STRIDE = 16;   // 16 longs = 128 bytes between slots (>= 64B cache line)
    static final int REPEATS = 3;   // best of N runs per variant

    // Opaque access: JIT may not hoist the memory access out of the loop,
    // but no expensive memory fences are added either.
    static final VarHandle VH = MethodHandles.arrayElementVarHandle(long[].class);

    interface Body { void run(int id); }

    /** Runs n threads released together; returns wall time in ms (start signal -> all joined). */
    static double timeThreads(int n, Body body) throws InterruptedException {
        CountDownLatch ready = new CountDownLatch(n);
        CountDownLatch go = new CountDownLatch(1);
        Thread[] threads = new Thread[n];
        for (int i = 0; i < n; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                ready.countDown();
                try { go.await(); } catch (InterruptedException e) { return; }
                body.run(id);
            });
            threads[i].start();
        }
        ready.await();
        long start = System.nanoTime();
        go.countDown();
        for (Thread t : threads) t.join();
        return (System.nanoTime() - start) / 1e6;
    }

    static double best(int n, java.util.function.Supplier<Body> makeBody,
                       Runnable reset, Runnable verify) throws InterruptedException {
        double best = Double.MAX_VALUE;
        for (int r = 0; r < REPEATS; r++) {
            reset.run();
            best = Math.min(best, timeThreads(n, makeBody.get()));
            verify.run();
        }
        return best;
    }

    public static void main(String[] args) throws Exception {
        final int n = args.length > 0 ? Integer.parseInt(args[0])
                                      : Runtime.getRuntime().availableProcessors();

        System.out.println("Student ID       : " + STUDENT_ID);
        System.out.println("OS               : " + System.getProperty("os.name") + " "
                + System.getProperty("os.version") + " (" + System.getProperty("os.arch") + ")");
        System.out.println("Java             : " + System.getProperty("java.version"));
        System.out.println("Logical cores    : " + Runtime.getRuntime().availableProcessors());
        System.out.println("Threads used (N) : " + n);
        System.out.println("Increments/thread: " + String.format("%,d", ITERATIONS));
        System.out.println("Best of          : " + REPEATS + " runs per variant");
        System.out.println();

        final long[] unpadded = new long[n];
        final long[] padded = new long[n * STRIDE];
        final long[] localOut = new long[n * STRIDE];

        // warm-up so the JIT compiles the loops before measuring
        timeThreads(n, id -> { long[] a = new long[n]; for (int k = 0; k < 2_000_000; k++) VH.setOpaque(a, id, (long) VH.getOpaque(a, id) + 1); });

        double tUnpadded = best(n, () -> id -> {
            for (long k = 0; k < ITERATIONS; k++)
                VH.setOpaque(unpadded, id, (long) VH.getOpaque(unpadded, id) + 1);
        }, () -> java.util.Arrays.fill(unpadded, 0L), () -> check(unpadded, 1, n));

        double tPadded = best(n, () -> id -> {
            final int idx = id * STRIDE;
            for (long k = 0; k < ITERATIONS; k++)
                VH.setOpaque(padded, idx, (long) VH.getOpaque(padded, idx) + 1);
        }, () -> java.util.Arrays.fill(padded, 0L), () -> check(padded, STRIDE, n));

        double tLocal = best(n, () -> id -> {
            long c = 0;
            for (long k = 0; k < ITERATIONS; k++) c++;
            localOut[id * STRIDE] = c;               // single write at the very end
        }, () -> java.util.Arrays.fill(localOut, 0L), () -> check(localOut, STRIDE, n));

        System.out.printf("%-34s | %12s%n", "Variant", "Wall Time (ms)");
        System.out.println("-".repeat(50));
        System.out.printf("%-34s | %12.3f%n", "Unpadded shared (false sharing)", tUnpadded);
        System.out.printf("%-34s | %12.3f%n", "Padded (128-byte stride)", tPadded);
        System.out.printf("%-34s | %12.3f%n", "Local variable, single write", tLocal);
        System.out.println();
        System.out.printf("Execution ratio  Unpadded / Padded : %.2fx%n", tUnpadded / tPadded);
        System.out.printf("Execution ratio  Unpadded / Local  : %.2fx%n", tUnpadded / Math.max(tLocal, 0.001));
        System.out.println("All counters verified = " + String.format("%,d", ITERATIONS) + " per thread");
    }

    static void check(long[] a, int stride, int n) {
        for (int i = 0; i < n; i++)
            if (a[i * stride] != ITERATIONS)
                throw new IllegalStateException("slot " + i + " = " + a[i * stride]);
    }
}