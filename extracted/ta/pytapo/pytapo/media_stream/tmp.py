import asyncio
import os
import subprocess
import json


class Streamer:
    def __init__(self, tapo, outputDirectory="/tmp/hls"):
        self.tapo = tapo
        self.outputDirectory = outputDirectory
        self.process = None

    async def start_hls(self):
        """Starts HLS stream using ffmpeg."""
        os.makedirs(self.outputDirectory, exist_ok=True)
        output_path = os.path.join(self.outputDirectory, "stream.m3u8")

        # Clean up old HLS files
        for f in os.listdir(self.outputDirectory):
            os.remove(os.path.join(self.outputDirectory, f))

        mediaSession = self.tapo.getMediaSession()
        async with mediaSession:
            payload = json.dumps(
                {
                    "type": "request",
                    "seq": 1,
                    "params": {
                        "preview": {
                            "audio": [],
                            "channels": [0],
                            "resolutions": ["HD"],
                        },
                        "method": "get",
                    },
                }
            )
            print(f"Starting HLS stream at: {self.outputDirectory}")

            self.process = subprocess.Popen(
                [
                    "ffmpeg",
                    "-loglevel",
                    "debug",
                    "-f",
                    "mpegts",  # Tell FFmpeg that input is MPEG-TS
                    "-i",
                    "pipe:0",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-f",
                    "hls",
                    "-hls_time",
                    "2",
                    "-hls_list_size",
                    "5",
                    "-hls_flags",
                    "delete_segments",
                    os.path.join(self.outputDirectory, "stream.m3u8"),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            async def log_ffmpeg():
                """Continuously print FFmpeg logs."""
                while True:
                    line = self.process.stderr.readline()
                    if not line:
                        break
                    print("[FFmpeg]", line.strip())

            asyncio.create_task(log_ffmpeg())

            print(f"FFmpeg PID: {self.process.pid}")

            async for resp in mediaSession.transceive(payload):
                print(resp)
                if resp.mimetype == "video/mp2t":
                    try:
                        print(
                            f"Writing {len(resp.plaintext)} bytes to FFmpeg stdin"
                        )  # Debugging
                        self.process.stdin.write(resp.plaintext)
                        self.process.stdin.flush()
                    except BrokenPipeError:
                        print("FFmpeg process closed unexpectedly.")
                        break  # Stop the loop if ffmpeg exits

            stderr_output = self.process.stderr.read().decode()
            print(stderr_output)  # Print FFmpeg errors

    def stop(self):
        """Stops the HLS stream."""
        if self.process:
            print("Stopping FFmpeg process...")
            self.process.terminate()
            self.process.wait()
            self.process = None
