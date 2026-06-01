import React, { useEffect, useRef, useState } from 'react';
import { Box, Text } from 'ink';
// [present, past] pairs
const MESSAGES = [
    ['Thinking', 'Thought'],
    ['Pondering', 'Pondered'],
    ['Calculating', 'Calculated'],
    ['Analyzing', 'Analyzed'],
    ['Processing', 'Processed'],
    ['Caramelizing onions', 'Caramelized onions'],
    ['Teaching a neural net to juggle', 'Taught a neural net to juggle'],
    ['Brewing coffee', 'Brewed coffee'],
    ['Asking GPT for help', 'Asked GPT for help'],
    ['Contemplating the universe', 'Contemplated the universe'],
    ['Debugging reality', 'Debugged reality'],
    ['Warming up the GPU', 'Warmed up the GPU'],
    ['Consulting the oracle', 'Consulted the oracle'],
    ['Counting electric sheep', 'Counted electric sheep'],
    ['Summoning AI spirits', 'Summoned AI spirits'],
    ['Bribing the LLM with RAM', 'Bribed the LLM with RAM'],
    ['Reticulating splines', 'Reticulated splines'],
    ['Feeding the hamster', 'Fed the hamster'],
    ['Aligning the chakras', 'Aligned the chakras'],
    ['Deciphering binary', 'Deciphered binary'],
    ['Teaching a cat to code', 'Taught a cat to code'],
    ['Charging the flux capacitor', 'Charged the flux capacitor'],
    ['Polishing the bits', 'Polished the bits'],
    ['Summoning Stack Overflow', 'Summoned Stack Overflow'],
    ['Compiling the compiler', 'Compiled the compiler'],
    ['Asking the rubber duck', 'Asked the rubber duck'],
    ['Warming up the qubits', 'Warmed up the qubits'],
    ['Negotiating with the GPU', 'Negotiated with the GPU'],
    ['Brewing a neural blend', 'Brewed a neural blend'],
    ['Defragmenting consciousness', 'Defragmented consciousness'],
    ['Synchronizing the multiverse', 'Synchronized the multiverse'],
    ['Rehearsing dad jokes', 'Rehearsed dad jokes'],
    ['Assembling IKEA instructions', 'Assembled IKEA instructions'],
    ['Flossing the dataset', 'Flossed the dataset'],
    ['Whispering to the weights', 'Whispered to the weights'],
    ['Calculating the meaning of 42', 'Calculated the meaning of 42'],
    ['Downloading more RAM', 'Downloaded more RAM'],
    ['Making a sandwich', 'Made a sandwich'],
    ['Convincing Skynet not to kill us', 'Convinced Skynet not to kill us'],
    ['Looking for the missing semicolon', 'Looked for the missing semicolon'],
    ['Untangling the spaghetti code', 'Untangled the spaghetti code'],
    ['Bribing the garbage collector', 'Bribed the garbage collector'],
    ['Asking Clippy for advice', 'Asked Clippy for advice'],
    ['Searching for a junior dev to blame', 'Searched for a junior dev to blame'],
    ['Rotating the 3D donut', 'Rotated the 3D donut'],
    ['Petting the attention heads', 'Petted the attention heads'],
    ["Sharpening Occam's razor", "Sharpened Occam's razor"],
    ['Herding the tokens', 'Herded the tokens'],
    ['Consulting the man page', 'Consulted the man page'],
    ['Reversing the polarity', 'Reversed the polarity'],
    ['Mining crypto on your CPU (jk)', 'Mined crypto on your CPU (jk)'],
    ['Teaching gradient descent to dance', 'Taught gradient descent to dance'],
    ['Counting to infinity, twice', 'Counted to infinity, twice'],
    ['Compressing the universe', 'Compressed the universe'],
    ['Dreaming in Python', 'Dreamed in Python'],
    ['Replacing tabs with spaces', 'Replaced tabs with spaces'],
    ['Rolling initiative', 'Rolled initiative'],
    ['Unfolding a paper crane recursively', 'Unfolded a paper crane recursively'],
    ['Running sudo rm -rf /doubts', 'Ran sudo rm -rf /doubts'],
    ['Updating node_modules', 'Updated node_modules'],
    ['Waiting for npm install', 'Waited for npm install'],
    ['Arguing with TypeScript', 'Argued with TypeScript'],
    ['Patching the kernel with duct tape', 'Patched the kernel with duct tape'],
    ['Rebooting the vibes', 'Rebooted the vibes'],
    ['Calibrating the sarcasm detector', 'Calibrated the sarcasm detector'],
    ['Generating a UUID (please wait)', 'Generated a UUID'],
    ['Blessing the registers', 'Blessed the registers'],
    ['Training on your browser history', 'Trained on your browser history'],
    ['Consulting the ancient docs', 'Consulted the ancient docs'],
    ['Loading the loading screen', 'Loaded the loading screen'],
    ['Asking ChatGPT to fix itself', 'Asked ChatGPT to fix itself'],
    ['Building in prod', 'Built in prod'],
    ['Pushing to main', 'Pushed to main'],
    ['Doing the needful', 'Did the needful'],
    ['Establishing a TCP handshake with the void', 'Established a TCP handshake with the void'],
];
const DOTS = ['·  ', '·· ', '···'];
const SHIMMER_HALF = 5; // half-width of shimmer spotlight in chars
// silver shimmer: base dim gray → bright silver/white at peak
function shimmerColor(dist) {
    if (dist >= SHIMMER_HALF)
        return '#484848';
    // quadratic falloff: 1 at center, 0 at edge
    const t = 1 - dist / SHIMMER_HALF;
    const ease = t * t;
    // interpolate from #484848 (72) to #f4f4f4 (244)
    const v = Math.round(72 + ease * 172);
    const hex = v.toString(16).padStart(2, '0');
    return `#${hex}${hex}${hex}`;
}
function shuffled(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}
export function ThinkingIndicator({ onCurrentPast }) {
    const [pairs] = useState(() => shuffled(MESSAGES));
    const [msgIdx, setMsgIdx] = useState(0);
    const [charCount, setCharCount] = useState(0);
    const [dotIdx, setDotIdx] = useState(0);
    // shimmerPos is a float: 0 = left edge of full string, sweeps right
    const [shimmerPos, setShimmerPos] = useState(-SHIMMER_HALF);
    const onCurrentPastRef = useRef(onCurrentPast);
    onCurrentPastRef.current = onCurrentPast;
    const [present, past] = pairs[msgIdx] ?? ['Thinking', 'Thought'];
    // advance to next message every 15 s (slower)
    useEffect(() => {
        const t = setInterval(() => {
            setMsgIdx((m) => (m + 1) % pairs.length);
            setCharCount(0);
            setDotIdx(0);
        }, 15000);
        return () => clearInterval(t);
    }, [pairs]);
    // notify parent whenever message changes
    useEffect(() => {
        onCurrentPastRef.current?.(past);
    }, [past]);
    // typing animation
    useEffect(() => { setCharCount(0); }, [msgIdx]);
    useEffect(() => {
        if (charCount >= present.length)
            return;
        const t = setTimeout(() => setCharCount((c) => c + 1), 45);
        return () => clearTimeout(t);
    }, [charCount, present]);
    // animate dots after fully typed
    useEffect(() => {
        if (charCount < present.length)
            return;
        const t = setInterval(() => setDotIdx((d) => (d + 1) % 3), 400);
        return () => clearInterval(t);
    }, [charCount, present.length]);
    // shimmer sweep: advances across the full string, loops
    const fullLen = 4 + present.length + 3; // "  ⟳ " + text + cursor (max)
    useEffect(() => {
        const t = setInterval(() => {
            setShimmerPos((p) => {
                const next = p + 0.55;
                return next > fullLen + SHIMMER_HALF ? -SHIMMER_HALF : next;
            });
        }, 50);
        return () => clearInterval(t);
    }, [fullLen]);
    const displayed = present.slice(0, charCount);
    const cursor = charCount < present.length ? '▌' : (DOTS[dotIdx] ?? '');
    const fullText = `  ⟳ ${displayed}${cursor}`;
    return (React.createElement(Box, null, Array.from(fullText).map((char, i) => (React.createElement(Text, { key: i, color: shimmerColor(Math.abs(i - shimmerPos)) }, char)))));
}
