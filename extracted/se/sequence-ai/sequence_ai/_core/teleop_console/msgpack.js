/* msgpack.js — msgpack as sequence_ai's msgpack_io writes it, both ways: unpack() reads one value back - an eval record's entries (eval-record.js) and what a robot says on a direct
   teleoperation connection (teleop-client.js) - and pack() writes what the console says to a robot, byte for byte as msgpack_io
   packs it.

   In one sentence: unpack(bytes) → the first byte says the type and how its length is written → strings as text, bytes as a
   Uint8Array over the same buffer (no copy: a camera's frames are most of a record and of a robot's messages), a map's keys strings
   whether written as str, bin (msgpack-numpy's b"nd") or int, every map an object with no prototype → the one value; arrayOf()
   makes a msgpack-numpy map an { dtype, shape, data } array; pack(value) → the smallest msgpack form of each int, every other
   number a double, strings as UTF-8, a Uint8Array as bin → bytes.

   WHY one module, every map without a prototype: the console read msgpack in two copies, and the eval record's copy built each map
   on a plain object, so a "__proto__" key in a record set that map's prototype instead of reading as a key; the teleoperation copy
   already built its maps with none. One reader now serves both, the stricter way each copy had: no prototype and every length
   checked against what is left (the teleoperation copy's), a key that is no string, bytes or integer refused and one error class
   (the record copy's).

   WHY written here and not a library: the console has no build step and loads nothing from outside its own origin (CSP
   script-src 'self'), and this much of msgpack is about 200 lines.

   WHY the same forms as msgpack_io: tools/check/test_teleop_msgpack.mjs compares these bytes with the bytes the SDK itself packs,
   so a console and a robot cannot drift apart.

   WHY no extension types and a depth limit on reading: what a record or a robot holds is data, and reading it runs nothing and
   cannot recurse without end.

   Numbers: JavaScript has one number type, so an integer-valued number packs as an int and any other as a double, and a 64-bit
   integer reads as the nearest double; a time on the wire is a whole count of microseconds since the epoch, about 1.7e15, inside
   the 2^53 a double holds exactly.

   Pure - no DOM, no requests - so node tests check it (frontend/tools/check/test_teleop_msgpack.mjs, test_eval_record.mjs). */

const MAX_DEPTH = 64;
const utf8 = new TextEncoder();
const text = new TextDecoder('utf-8', { fatal: true });

/* What pack() and unpack() throw: a value that cannot be sent, or bytes that are not one msgpack value of the kinds read here. */
export class MsgpackError extends Error {}

/* A growing buffer of bytes and the big-endian writes msgpack is made of. */
class Out {
  constructor() {
    this.bytes = new Uint8Array(256);
    this.view = new DataView(this.bytes.buffer);
    this.at = 0;
  }

  // room for n more bytes, doubling so a large step costs a few copies
  room(n) {
    if (this.at + n <= this.bytes.length) return;
    let size = this.bytes.length * 2;
    while (size < this.at + n) size *= 2;
    const next = new Uint8Array(size);
    next.set(this.bytes.subarray(0, this.at));
    this.bytes = next;
    this.view = new DataView(next.buffer);
  }

  u8(v) { this.room(1); this.view.setUint8(this.at, v); this.at += 1; }

  u16(v) { this.room(2); this.view.setUint16(this.at, v); this.at += 2; }

  u32(v) { this.room(4); this.view.setUint32(this.at, v); this.at += 4; }

  f64(v) { this.room(8); this.view.setFloat64(this.at, v); this.at += 8; }

  // a 64-bit integer, in two halves: a double cannot be handed to setUint32 past 2^32, and BigInt is not needed for what is safe
  u64(v) {
    const hi = Math.floor(v / 2 ** 32);
    this.u32(hi >>> 0);
    this.u32((v - hi * 2 ** 32) >>> 0);
  }

  raw(b) { this.room(b.length); this.bytes.set(b, this.at); this.at += b.length; }
}

/* An integer in the smallest form that holds it, as _pack_int chooses: positive fixint, negative fixint, then 8, 16, 32, 64 bits. */
function packInt(n, out) {
  if (n >= 0 && n <= 0x7f) out.u8(n);
  else if (n >= -32 && n < 0) out.u8(n + 0x100);
  else if (n > 0) {
    if (n <= 0xff) { out.u8(0xcc); out.u8(n); }
    else if (n <= 0xffff) { out.u8(0xcd); out.u16(n); }
    else if (n <= 0xffffffff) { out.u8(0xce); out.u32(n); }
    else { out.u8(0xcf); out.u64(n); }
  } else if (n >= -0x80) { out.u8(0xd0); out.u8(n + 0x100); }
  else if (n >= -0x8000) { out.u8(0xd1); out.u16(n + 0x10000); }
  else if (n >= -0x80000000) { out.u8(0xd2); out.u32(n + 2 ** 32); }
  else {
    // two's complement of a 64-bit value, in halves: the low half is n's own, the high half what is left, both unsigned
    out.u8(0xd3);
    const hi = Math.floor(n / 2 ** 32);
    out.u32(hi >>> 0);
    out.u32((n - hi * 2 ** 32) >>> 0);
  }
}

/* A length in the smallest head that holds it: `fix` a [base, most] for the forms with one, `sizes` each [code, bits]. */
function packHead(n, out, fix, sizes, what) {
  if (fix && n <= fix[1]) { out.u8(fix[0] | n); return; }
  for (const [code, bits] of sizes) {
    if (n < 2 ** bits) {
      out.u8(code);
      if (bits === 8) out.u8(n); else if (bits === 16) out.u16(n); else out.u32(n);
      return;
    }
  }
  throw new MsgpackError(`a ${what} of ${n}: past msgpack's 32-bit lengths`);
}

function packValue(value, out, depth) {
  if (depth > MAX_DEPTH) throw new MsgpackError(`nested deeper than ${MAX_DEPTH} levels`);
  if (value === null || value === undefined) out.u8(0xc0);
  else if (value === true) out.u8(0xc3);
  else if (value === false) out.u8(0xc2);
  else if (typeof value === 'number') {
    if (Number.isSafeInteger(value)) packInt(value, out);
    else { out.u8(0xcb); out.f64(value); }     // a fraction, or a whole number a double no longer holds exactly
  } else if (typeof value === 'string') {
    const raw = utf8.encode(value);
    packHead(raw.length, out, [0xa0, 31], [[0xd9, 8], [0xda, 16], [0xdb, 32]], 'string');
    out.raw(raw);
  } else if (value instanceof Uint8Array) {
    packHead(value.length, out, null, [[0xc4, 8], [0xc5, 16], [0xc6, 32]], 'bytes');
    out.raw(value);
  } else if (Array.isArray(value)) {
    packHead(value.length, out, [0x90, 15], [[0xdc, 16], [0xdd, 32]], 'list');
    for (const item of value) packValue(item, out, depth + 1);
  } else if (typeof value === 'object') {
    const keys = Object.keys(value);
    packHead(keys.length, out, [0x80, 15], [[0xde, 16], [0xdf, 32]], 'map');
    for (const key of keys) {
      packValue(key, out, depth + 1);
      packValue(value[key], out, depth + 1);
    }
  } else {
    throw new MsgpackError(`a ${typeof value} cannot be sent as msgpack`);
  }
}

/* `value` as msgpack: null, booleans, numbers, strings, Uint8Array, arrays and objects at any depth up to MAX_DEPTH. */
export function pack(value) {
  const out = new Out();
  packValue(value, out, 0);
  return out.bytes.slice(0, out.at);
}

/* Each fixed-size value by its code: its read and how many bytes it takes. */
const FIXED = {
  0xcc: [(v, i) => v.getUint8(i), 1],
  0xcd: [(v, i) => v.getUint16(i), 2],
  0xce: [(v, i) => v.getUint32(i), 4],
  0xcf: [(v, i) => v.getUint32(i) * 2 ** 32 + v.getUint32(i + 4), 8],
  0xd0: [(v, i) => v.getInt8(i), 1],
  0xd1: [(v, i) => v.getInt16(i), 2],
  0xd2: [(v, i) => v.getInt32(i), 4],
  0xd3: [(v, i) => v.getInt32(i) * 2 ** 32 + v.getUint32(i + 4), 8],
  0xca: [(v, i) => v.getFloat32(i), 4],
  0xcb: [(v, i) => v.getFloat64(i), 8],
};
/* Each sized value by its code: its kind and how many bytes its length takes. */
const SIZED = {
  0xc4: ['bin', 1], 0xc5: ['bin', 2], 0xc6: ['bin', 4],
  0xd9: ['str', 1], 0xda: ['str', 2], 0xdb: ['str', 4],
  0xdc: ['list', 2], 0xdd: ['list', 4],
  0xde: ['map', 2], 0xdf: ['map', 4],
};

/* Reads one value from `bytes`: `at` where the next byte is. Every length is checked against what is left, so bytes cut short or
   made up throw rather than reading past their end. */
class Reader {
  constructor(bytes) {
    this.bytes = bytes;
    this.view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    this.at = 0;
  }

  take(n) {
    if (this.at + n > this.bytes.length) {
      throw new MsgpackError(`the msgpack ends inside a value: ${n} bytes asked for at ${this.at} of ${this.bytes.length}`);
    }
    const from = this.at;
    this.at += n;
    return from;
  }

  length(n) {
    const i = this.take(n);
    return n === 1 ? this.view.getUint8(i) : n === 2 ? this.view.getUint16(i) : this.view.getUint32(i);
  }

  string(n) {
    const from = this.take(n);
    return text.decode(this.bytes.subarray(from, from + n));
  }

  list(n, depth) {
    // every item takes a byte at least: no list longer than what is left
    if (n > this.bytes.length - this.at) throw new MsgpackError(`a list of ${n} items where ${this.bytes.length - this.at} bytes are left`);
    const out = new Array(n);
    for (let i = 0; i < n; i += 1) out[i] = this.read(depth + 1);
    return out;
  }

  map(n, depth) {
    if (n * 2 > this.bytes.length - this.at) throw new MsgpackError(`a map of ${n} items where ${this.bytes.length - this.at} bytes are left`);
    // no prototype: a key a record or a robot holds is data, and "__proto__" on a plain object would set one
    const out = Object.create(null);
    for (let i = 0; i < n; i += 1) {
      const key = this.read(depth + 1);
      // bytes keys read as UTF-8 (msgpack-numpy's are), an integer key as its digits; any other key is no name here
      const name = key instanceof Uint8Array ? text.decode(key) : typeof key === 'string' || typeof key === 'number' ? String(key) : null;
      if (name === null) throw new MsgpackError('a map key that is not a string, bytes or an integer');
      out[name] = this.read(depth + 1);
    }
    return out;
  }

  read(depth) {
    if (depth > MAX_DEPTH) throw new MsgpackError(`nested deeper than ${MAX_DEPTH} levels`);
    const code = this.bytes[this.take(1)];
    if (code <= 0x7f) return code;
    if (code >= 0xe0) return code - 0x100;
    if (code >= 0xa0 && code <= 0xbf) return this.string(code & 0x1f);
    if (code >= 0x90 && code <= 0x9f) return this.list(code & 0x0f, depth);
    if (code >= 0x80 && code <= 0x8f) return this.map(code & 0x0f, depth);
    if (code === 0xc0) return null;
    if (code === 0xc2) return false;
    if (code === 0xc3) return true;
    const fixed = FIXED[code];
    if (fixed) return fixed[0](this.view, this.take(fixed[1]));
    const sized = SIZED[code];
    if (sized) {
      const n = this.length(sized[1]);
      if (sized[0] === 'str') return this.string(n);
      if (sized[0] === 'list') return this.list(n, depth);
      if (sized[0] === 'map') return this.map(n, depth);
      const from = this.take(n);
      return this.bytes.subarray(from, from + n);
    }
    throw new MsgpackError(`msgpack type 0x${code.toString(16)} is not read here (extension types and the unused code)`);
  }
}

/* The one msgpack value `bytes` (a Uint8Array) holds; throws MsgpackError for one cut short, more than one value, an extension
   type, a key that is no name or too deep a nesting. */
export function unpack(bytes) {
  const reader = new Reader(bytes);
  const value = reader.read(0);
  if (reader.at !== bytes.length) throw new MsgpackError(`${bytes.length - reader.at} bytes follow the msgpack value`);
  return value;
}

/* A msgpack-numpy map as { dtype, shape, data } - dtype numpy's string for it ("|u1", "<u2", "<f4"), data its bytes in C
   order - or null for any other value. */
export function arrayOf(m) {
  if (!m || typeof m !== 'object' || m.nd !== true || typeof m.type !== 'string' || !Array.isArray(m.shape)
    || !(m.data instanceof Uint8Array)) return null;
  return { dtype: m.type, shape: m.shape, data: m.data };
}
