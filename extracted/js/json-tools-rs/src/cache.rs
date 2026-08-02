//! Multi-tier caching for regex patterns.
//!
//! Three-tier regex cache: compile-time table for common patterns, thread-local
//! FxHashMap for recent patterns, and global RwLock<FxHashMap> for shared access.

use crate::fxhash::FxHashMap;
use regex::Regex;
use smallvec::SmallVec;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, LazyLock, RwLock};

/// Monotonic "recency" counter shared by both cache tiers, so eviction can identify
/// the genuinely least-recently-used entry instead of an arbitrary one. A plain
/// `fetch_add` is cheap enough to call on every cache hit; eviction only scans for
/// the minimum tick when the cache is actually full, which is the already-rare path
/// (a cache miss followed by a `Regex::new` compile costs far more than an O(n) scan
/// over at most a few hundred entries).
static CACHE_CLOCK: AtomicU64 = AtomicU64::new(0);

#[inline]
fn next_tick() -> u64 {
    CACHE_CLOCK.fetch_add(1, Ordering::Relaxed)
}

/// Maximum number of patterns in the thread-local cache before eviction.
const THREAD_LOCAL_CACHE_CAPACITY: usize = 128;

/// Maximum number of patterns in the global `RwLock<FxHashMap>` cache.
const GLOBAL_CACHE_CAPACITY: usize = 512;

/// Pre-compiled common regex patterns for maximum performance
/// Using Arc<Regex> to make cloning O(1) instead of copying the entire regex state
/// Using std::sync::LazyLock (Rust 1.80+) instead of lazy_static for better performance
static COMMON_REGEX_PATTERNS: LazyLock<FxHashMap<&'static str, Arc<Regex>>> = LazyLock::new(|| {
    // Pre-allocate with increased capacity for expanded pattern set
    let mut patterns = FxHashMap::with_capacity_and_hasher(50, Default::default());

    // Common patterns for key/value replacements
    let common_patterns = [
        // Whitespace patterns
        (r"\s+", "Multiple whitespace"),
        (r"^\s+|\s+$", "Leading/trailing whitespace"),
        (r"\s", "Any whitespace"),
        (r"\n+", "Multiple newlines"),
        (r"\r\n", "Windows line ending"),
        // Special character patterns
        (r"[^\w\s]", "Non-word, non-space characters"),
        (r"[^a-zA-Z0-9]", "Non-alphanumeric"),
        (r"[^a-zA-Z0-9_]", "Non-alphanumeric except underscore"),
        (
            r"[^a-zA-Z0-9_-]",
            "Non-alphanumeric except underscore and hyphen",
        ),
        // Common JSON key patterns
        (r"[A-Z]", "Uppercase letters"),
        (r"[a-z]", "Lowercase letters"),
        (r"\d+", "Digits"),
        (r"_+", "Multiple underscores"),
        (r"-+", "Multiple hyphens"),
        (r"\.+", "Multiple dots"),
        // Email and URL patterns (common in JSON data)
        (r"@", "At symbol (emails)"),
        (r"\.", "Dot (domains, decimals)"),
        (r"://", "Protocol separator"),
        (r"https?://", "HTTP/HTTPS protocol"),
        // Date/time patterns
        (r"\d{4}-\d{2}-\d{2}", "ISO date (YYYY-MM-DD)"),
        (r"\d{2}:\d{2}:\d{2}", "Time format (HH:MM:SS)"),
        (r"\d{4}/\d{2}/\d{2}", "US date format (YYYY/MM/DD)"),
        (r"\d{2}/\d{2}/\d{4}", "Date format (MM/DD/YYYY)"),
        // UUID patterns
        (
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
            "UUID format",
        ),
        (r"[0-9a-fA-F]{32}", "UUID without hyphens"),
        // IP address patterns
        (r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "IPv4 address"),
        (r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}", "IPv6 address"),
        // Naming convention patterns
        (r"[a-z]+([A-Z][a-z]+)*", "camelCase"),
        (r"[a-z]+(_[a-z]+)*", "snake_case"),
        (r"[a-z]+(-[a-z]+)*", "kebab-case"),
        (r"[A-Z]+([A-Z][a-z]+)*", "PascalCase"),
        // Currency patterns
        (r"\$\d+(\.\d{2})?", "USD currency"),
        (r"€\d+(\.\d{2})?", "EUR currency"),
        (r"£\d+(\.\d{2})?", "GBP currency"),
        (r"\d+(\.\d{2})?\s*(USD|EUR|GBP)", "Currency with code"),
        // Version number patterns
        (r"\d+\.\d+\.\d+", "Semantic version"),
        (r"v\d+\.\d+", "Version prefix"),
        // File and path patterns
        (r"\.\w+$", "File extension"),
        (r"/[^/]+", "Path segment"),
        (r"\\[^\\]+", "Windows path segment"),
        // Bracket and quote patterns
        (r"\[.*?\]", "Square brackets with content"),
        (r"\{.*?\}", "Curly braces with content"),
        (r"\(.*?\)", "Parentheses with content"),
        (r#"".*?""#, "Double quoted string"),
        (r"'.*?'", "Single quoted string"),
        // Common user patterns for key/value replacements
        (r"^(user|admin)_", "User/admin prefix"),
        (r"^(User|Admin)_", "User/Admin prefix (capitalized)"),
        (r"(user|admin)_", "User/admin anywhere"),
        (r"(User|Admin)_", "User/Admin anywhere (capitalized)"),
        (r"@example\.com", "Example email domain"),
        (r"@example\.org", "Example org domain"),
        (r"@company\.org", "Company org domain"),
        (r"@company\.com", "Company com domain"),
        (r"_id$", "Trailing _id suffix"),
        (r"_ids$", "Trailing _ids suffix"),
        (r"^id_", "Leading id_ prefix"),
        (r"_at$", "Timestamp suffix (_at)"),
        (r"_on$", "Date suffix (_on)"),
        (r"^created_", "Created prefix"),
        (r"^updated_", "Updated prefix"),
        (r"^deleted_", "Deleted prefix"),
        (r"^is_", "Boolean prefix (is_)"),
        (r"^has_", "Boolean prefix (has_)"),
        (r"^can_", "Boolean prefix (can_)"),
    ];

    for (pattern, _) in &common_patterns {
        if let Ok(regex) = Regex::new(pattern) {
            patterns.insert(*pattern, Arc::new(regex));
        }
    }

    patterns
});

/// Cached regex plus its last-access tick, for LRU eviction. The tick lives outside
/// the `Arc<Regex>` (rather than e.g. inside a wrapper struct) so it can be bumped
/// through a shared reference -- readers only need a *read* lock on the outer map to
/// record a cache hit, not a write lock.
type CacheEntry = (Arc<Regex>, AtomicU64);

static REGEX_CACHE: LazyLock<RwLock<FxHashMap<Arc<str>, CacheEntry>>> = LazyLock::new(|| {
    RwLock::new(FxHashMap::with_capacity_and_hasher(
        GLOBAL_CACHE_CAPACITY,
        Default::default(),
    ))
});

thread_local! {
    static THREAD_LOCAL_REGEX_CACHE: std::cell::RefCell<FxHashMap<Arc<str>, CacheEntry>> =
        std::cell::RefCell::new(FxHashMap::with_capacity_and_hasher(THREAD_LOCAL_CACHE_CAPACITY, Default::default()));
}

/// Evict the least-recently-used half of a thread-local cache (batched, rather than
/// evicting one entry per insert, to amortize the O(n) scan across future inserts).
#[inline]
fn evict_thread_local_lru_half(cache: &mut FxHashMap<Arc<str>, CacheEntry>) {
    let mut ticks: Vec<u64> = cache
        .values()
        .map(|(_, tick)| tick.load(Ordering::Relaxed))
        .collect();
    ticks.sort_unstable();
    let median = ticks[ticks.len() / 2];
    cache.retain(|_, (_, tick)| tick.load(Ordering::Relaxed) >= median);
}

/// Insert a regex into the thread-local cache, evicting if at capacity.
#[inline]
fn insert_thread_local(pattern: &str, regex: &Arc<Regex>) {
    THREAD_LOCAL_REGEX_CACHE.with(|cache| {
        let mut cache_ref = cache.borrow_mut();
        if cache_ref.len() >= THREAD_LOCAL_CACHE_CAPACITY {
            evict_thread_local_lru_half(&mut cache_ref);
        }
        cache_ref.insert(
            Arc::from(pattern),
            (Arc::clone(regex), AtomicU64::new(next_tick())),
        );
    });
}

/// Capacity of the sticky fast-path cache (see `STICKY_REGEX_CACHE`'s doc comment).
/// `ReplacementConfig` is itself sized for 0-2 patterns per key/value list (see its
/// doc comment); 4 gives headroom for a key-replacement pattern and a
/// value-replacement pattern both being in flight on the same thread without
/// thrashing, while staying small enough that the linear scan stays cheap.
const STICKY_CACHE_CAPACITY: usize = 4;

/// Storage type for the sticky cache -- named to avoid a `clippy::type_complexity`
/// warning on the `thread_local!` declaration below.
type StickyCache = SmallVec<[(Arc<str>, Arc<Regex>); STICKY_CACHE_CAPACITY]>;

thread_local! {
    /// Tiny "sticky" fast-path cache checked before the thread-local/global tiers: a
    /// plain linear scan over a handful of recently-used `(pattern, regex)` pairs,
    /// comparing pattern strings directly instead of hashing them. The *same*
    /// `ProcessingConfig` -- and thus the same, small pattern list -- is reused for
    /// every key/value across an entire `execute()` call (potentially a large batch
    /// under parallel dispatch), so after the first call this almost always hits.
    ///
    /// Found via sampling profiler (`sample`/`samply` against a release build with
    /// debug symbols): `get_cached_regex` was the single largest hotspot (by a wide
    /// margin -- roughly a fifth of all samples) in a batch/parallel workload with a
    /// regex `key_replacement` configured, because every single key check re-hashed
    /// the pattern string and walked the thread-local `FxHashMap` (tier 2) from
    /// scratch even though the same pattern had just been resolved on the immediately
    /// preceding call. A short linear scan over full pattern strings (no hashing at
    /// all) is cheaper than one hash computation plus a hashmap probe for the
    /// realistic 1-2-distinct-pattern case, and sidesteps the tier-2 `RefCell` borrow
    /// and hashing entirely on a hit.
    static STICKY_REGEX_CACHE: std::cell::RefCell<StickyCache> =
        std::cell::RefCell::new(SmallVec::new());
}

/// Insert into the sticky cache, evicting the oldest entry (FIFO) if at capacity.
/// Not a full LRU: with a capacity of just 4 entries existing purely to catch
/// immediate repeated use, precise recency tracking would cost more than the miss
/// it's avoiding.
#[inline]
fn insert_sticky(pattern: &str, regex: &Arc<Regex>) {
    STICKY_REGEX_CACHE.with(|cache| {
        let mut cache = cache.borrow_mut();
        if cache.iter().any(|(p, _)| p.as_ref() == pattern) {
            return; // already present
        }
        if cache.len() >= STICKY_CACHE_CAPACITY {
            cache.remove(0);
        }
        cache.push((Arc::from(pattern), Arc::clone(regex)));
    });
}

/// A key/value replacement pattern is either a regex (explicitly marked by wrapping it in
/// `r'...'`, e.g. `r'^admin_'`) or a literal string to match exactly. Bare patterns are
/// literal -- there is no implicit "try regex, fall back to literal" behavior, so a pattern
/// containing characters that happen to be regex metacharacters (`.`, `$`, `(`, etc.) always
/// matches literally unless explicitly wrapped.
pub(crate) enum ParsedPattern<'a> {
    Regex(&'a str),
    Literal(&'a str),
}

/// Parse a replacement pattern into its literal or regex form. See `ParsedPattern`.
#[inline]
pub(crate) fn parse_pattern(pattern: &str) -> ParsedPattern<'_> {
    if pattern.len() >= 3 && pattern.starts_with("r'") && pattern.ends_with('\'') {
        ParsedPattern::Regex(&pattern[2..pattern.len() - 1])
    } else {
        ParsedPattern::Literal(pattern)
    }
}

/// Get a cached regex, using Arc<Regex> for O(1) cloning
///
/// Three-tier caching strategy (optimized for both latency and concurrency):
/// 1. Pre-compiled common patterns (static, no allocation)
/// 2. Thread-local cache (lock-free, thread-specific)
/// 3. Global RwLock<FxHashMap> (shared across threads)
pub(crate) fn get_cached_regex(pattern: &str) -> Result<Arc<Regex>, regex::Error> {
    // TIER 1: Check pre-compiled common patterns (fastest path, no allocation)
    if let Some(regex) = COMMON_REGEX_PATTERNS.get(pattern) {
        return Ok(Arc::clone(regex));
    }

    // STICKY: tiny linear-scan cache of recently-used patterns -- see its doc comment.
    let sticky_hit = STICKY_REGEX_CACHE.with(|cache| {
        cache
            .borrow()
            .iter()
            .find(|(p, _)| p.as_ref() == pattern)
            .map(|(_, r)| Arc::clone(r))
    });
    if let Some(regex) = sticky_hit {
        return Ok(regex);
    }

    // TIER 2: Try thread-local cache (fast path, no locks)
    let thread_local_result = THREAD_LOCAL_REGEX_CACHE.with(|cache| {
        let cache_ref = cache.borrow();
        cache_ref.get(pattern).map(|(regex, tick)| {
            tick.store(next_tick(), Ordering::Relaxed);
            Arc::clone(regex)
        })
    });

    if let Some(regex) = thread_local_result {
        insert_sticky(pattern, &regex);
        return Ok(regex);
    }

    // TIER 3: Try global cache under read lock
    {
        if let Some((regex, tick)) = REGEX_CACHE.read().unwrap().get(pattern) {
            tick.store(next_tick(), Ordering::Relaxed);
            let regex_arc = Arc::clone(regex);
            insert_thread_local(pattern, &regex_arc);
            insert_sticky(pattern, &regex_arc);
            return Ok(regex_arc);
        }
    }

    // NOT FOUND: Compile before taking the write lock (expensive operation)
    let regex = Arc::new(Regex::new(pattern)?);

    {
        let mut cache = REGEX_CACHE.write().unwrap();
        // Another thread may have compiled the same pattern while we were waiting
        if let Some((existing, tick)) = cache.get(pattern) {
            tick.store(next_tick(), Ordering::Relaxed);
            let existing_arc = Arc::clone(existing);
            insert_sticky(pattern, &existing_arc);
            return Ok(existing_arc);
        }
        // Bounded cache: evict the genuinely least-recently-used entry if at capacity
        if cache.len() >= GLOBAL_CACHE_CAPACITY {
            if let Some(lru_key) = cache
                .iter()
                .min_by_key(|(_, (_, tick))| tick.load(Ordering::Relaxed))
                .map(|(k, _)| k.clone())
            {
                cache.remove(&lru_key);
            }
        }
        cache.insert(
            Arc::from(pattern),
            (Arc::clone(&regex), AtomicU64::new(next_tick())),
        );
    }

    insert_thread_local(pattern, &regex);
    insert_sticky(pattern, &regex);
    Ok(regex)
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The thread-local cache tier must evict genuinely least-recently-used entries,
    /// not an arbitrary half -- regression test for the previous alternating-retain
    /// eviction, which had no concept of recency and could evict a pattern being
    /// accessed on every single call just as readily as one never touched again.
    ///
    /// Scoped to the thread-local tier deliberately: each `#[test]` fn runs on its own
    /// thread, so this tier's state is naturally isolated from other tests running
    /// concurrently. The global tier shares the same tick-based eviction logic but is
    /// process-wide, so asserting on it here would risk flakiness from unrelated tests'
    /// cache activity.
    /// Test-only: check the thread-local tier directly, bypassing the tier-1/tier-3
    /// fallbacks that `get_cached_regex` would otherwise use to mask an eviction from
    /// this tier specifically (the global tier has its own, much larger capacity and
    /// won't have evicted the same entry, so a `get_cached_regex` call alone can't
    /// distinguish "still in the thread-local cache" from "fell through to tier 3").
    fn thread_local_cache_contains(pattern: &str) -> bool {
        THREAD_LOCAL_REGEX_CACHE.with(|cache| cache.borrow().contains_key(pattern))
    }

    #[test]
    fn test_thread_local_cache_evicts_lru_not_arbitrary() {
        let hot_pattern = "lru_test_hot_pattern_zzz";
        get_cached_regex(hot_pattern).expect("hot pattern should compile");

        let cold_pattern = "lru_test_cold_pattern_zzz";
        get_cached_regex(cold_pattern).expect("cold pattern should compile");

        assert!(thread_local_cache_contains(hot_pattern));
        assert!(thread_local_cache_contains(cold_pattern));

        // Flood well past THREAD_LOCAL_CACHE_CAPACITY with distinct patterns, periodically
        // re-touching the hot pattern to keep its tick fresh. The cold pattern is never
        // touched again after its initial compile above.
        for i in 0..(THREAD_LOCAL_CACHE_CAPACITY * 3) {
            let pattern = format!("lru_test_flood_pattern_{i}");
            get_cached_regex(&pattern).expect("flood pattern should compile");
            if i % 4 == 0 {
                get_cached_regex(hot_pattern).expect("hot pattern re-access should succeed");
            }
        }

        assert!(
            thread_local_cache_contains(hot_pattern),
            "repeatedly-accessed pattern should survive eviction"
        );
        assert!(
            !thread_local_cache_contains(cold_pattern),
            "untouched pattern should have been evicted, not kept by arbitrary chance"
        );
    }

    /// Regression test for the sticky fast-path cache (`STICKY_REGEX_CACHE`,
    /// `insert_sticky`): interleaving more distinct patterns than
    /// `STICKY_CACHE_CAPACITY` on one thread must never return the wrong regex for
    /// a given pattern, even once the sticky slots have cycled through eviction.
    /// Each pattern here is distinct enough (different literal text matched) that
    /// a mixed-up regex would produce an observably wrong `is_match` result, not
    /// just an internal inconsistency.
    #[test]
    fn test_sticky_cache_no_cross_contamination_across_eviction() {
        // More distinct patterns than STICKY_CACHE_CAPACITY, each matching only its
        // own distinct literal text.
        let patterns_and_targets: Vec<(String, &str)> = (0..(STICKY_CACHE_CAPACITY * 3))
            .map(|i| (format!("^sticky_test_marker_{i}$"), "irrelevant"))
            .collect();

        // First pass: compile every pattern once each, evicting earlier ones out of
        // the sticky slots as later ones are inserted.
        for (pattern, _) in &patterns_and_targets {
            get_cached_regex(pattern).expect("pattern should compile");
        }

        // Second pass: re-fetch every pattern (a mix of sticky hits for the most
        // recent few, and thread-local/global fallback for the rest) and confirm
        // each one only matches its *own* target text, never another pattern's.
        for (i, (pattern, _)) in patterns_and_targets.iter().enumerate() {
            let regex = get_cached_regex(pattern).expect("re-fetch should succeed");
            let own_text = format!("sticky_test_marker_{i}");
            assert!(
                regex.is_match(&own_text),
                "pattern {pattern:?} should match its own marker text"
            );
            // Spot-check against a neighboring pattern's text to catch cross-contamination.
            let other_i = (i + 1) % patterns_and_targets.len();
            let other_text = format!("sticky_test_marker_{other_i}");
            if other_i != i {
                assert!(
                    !regex.is_match(&other_text),
                    "pattern {pattern:?} must not match a different marker's text \
                     ({other_text:?}) -- indicates sticky-cache cross-contamination"
                );
            }
        }
    }
}
