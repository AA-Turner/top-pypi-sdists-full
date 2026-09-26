import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import path from "node:path";
import { Readable } from "node:stream";
import test from "node:test";

// Check the copy NestJS actually loads, including nested dependency installs.
const require = createRequire(import.meta.url);
const nestRequire = createRequire(
  require.resolve("@nestjs/platform-express/package.json"),
);
const multer = nestRequire("multer");

function upload(middleware, fields = [{ name: "file", content: "benchmark" }]) {
  const boundary = "benchmark-multer-test";
  const body = Buffer.from(
    fields
      .map(
        ({ name, content }) =>
          `--${boundary}\r\nContent-Disposition: form-data; name="${name}"; filename="result.txt"\r\nContent-Type: text/plain\r\n\r\n${content}\r\n`,
      )
      .join("") + `--${boundary}--\r\n`,
  );
  const req = Readable.from([body]);
  req.headers = {
    "content-type": `multipart/form-data; boundary=${boundary}`,
    "content-length": String(body.length),
  };
  return new Promise((resolve, reject) => {
    middleware(req, {}, (error) => (error ? reject(error) : resolve(req)));
  });
}

test("NestJS resolves patched Multer 2.x", () => {
  const [major, minor] = nestRequire("multer/package.json")
    .version.split(".")
    .map(Number);
  assert.equal(major, 2);
  assert.ok(
    minor >= 3,
    "Multer must be >=2.3.0 to address the benchmark alerts",
  );
});

test("single uploads preserve memory storage and fileFilter callbacks", async () => {
  let filtered = false;
  const req = await upload(
    multer({
      limits: { fileSize: 1024, files: 1, fields: 1 },
      fileFilter: (_req, file, done) => {
        filtered = true;
        assert.equal(file.originalname, "result.txt");
        done(null, true);
      },
    }).single("file"),
  );
  assert.ok(filtered);
  assert.equal(req.file.buffer.toString(), "benchmark");
});

for (const mode of ["array", "fields", "any"]) {
  test(`${mode} uploads preserve the API used by NestJS interceptors`, async () => {
    const parser = multer({ limits: { fileSize: 1024, files: 1 } });
    const middleware =
      mode === "array"
        ? parser.array("file", 1)
        : mode === "fields"
          ? parser.fields([{ name: "file", maxCount: 1 }])
          : parser.any();
    const req = await upload(middleware);
    const files = mode === "fields" ? req.files.file : req.files;
    assert.equal(files.length, 1);
    assert.equal(files[0].buffer.toString(), "benchmark");
  });
}

test("disk storage preserves uploaded file contents", async () => {
  const directory = await mkdtemp(path.join(tmpdir(), "benchmark-multer-"));
  try {
    const req = await upload(
      multer({ dest: directory, limits: { fileSize: 1024 } }).single("file"),
    );
    assert.equal(await readFile(req.file.path, "utf8"), "benchmark");
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("oversized files still return a MulterError", async () => {
  await assert.rejects(
    upload(multer({ limits: { fileSize: 2 } }).single("file")),
    (error) =>
      error instanceof multer.MulterError && error.code === "LIMIT_FILE_SIZE",
  );
});

test("unexpected fields still return a MulterError", async () => {
  await assert.rejects(
    upload(multer().single("expected")),
    (error) =>
      error instanceof multer.MulterError &&
      error.code === "LIMIT_UNEXPECTED_FILE",
  );
});

test("fileFilter rejection does not retain a file", async () => {
  const req = await upload(
    multer({ fileFilter: (_req, _file, done) => done(null, false) }).single(
      "file",
    ),
  );
  assert.equal(req.file, undefined);
});
