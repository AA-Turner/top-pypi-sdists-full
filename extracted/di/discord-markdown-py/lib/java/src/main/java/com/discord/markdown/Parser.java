package com.discord.markdown;

public class Parser {
    static {
        System.loadLibrary("discord_markdown");
    }

    public static native String parseToAstString(String input);
}
