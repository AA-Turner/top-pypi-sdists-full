import com.discord.markdown.Parser;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;

public class Test {
    static long max = 0;
    static long maxRun = 0;
    static long min = Integer.MAX_VALUE;
    static long minRun = 0;
    static long running = 0;

    public static void main(String[] args) throws IOException {
//        String rawContent = "_foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_";
//        String rawContent = "_foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_";
        String rawContent = String.join("", Files.readAllLines(Paths.get("../../test_content/discordjs_announcement/content.md")));

        testParse(rawContent, -1);
        testParse(rawContent, -1);
        testParse(rawContent, -1);
        testParse(rawContent, -1);
        testParse(rawContent, -1);

        int totalRuns = 3000;
        for (int i =- 0; i < totalRuns; i++) {
            testParse(rawContent, i);
        }

        System.out.printf("max=%d, maxRun=%d, min=%d, minRun=%d, avg=%d\n", max/1000, maxRun, min/1000, minRun, (running/totalRuns) / 1000);
    }

    public static void testParse(String rawContent, int currentRun) throws IOException {
        long startTime = System.nanoTime();
        String parsed = Parser.parseToAstString(rawContent);
        long endTime = System.nanoTime();
        long elapsedTime = endTime - startTime;

//        System.out.println("Elapsed time: " + elapsedTime/1000 + "micros");
        System.out.println(parsed);
//        System.out.println();

        if (currentRun < 0) {
            return;
        }

        if (max < elapsedTime) {
            max = elapsedTime;
            maxRun = currentRun;
        }
        if (min > elapsedTime) {
            min = elapsedTime;
            minRun = currentRun;
        }
        running += elapsedTime;
    }
}
