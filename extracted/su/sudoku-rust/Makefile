clean:
	cargo clean
	uv cache clear
	pytest --cache-clear

check:
	cargo clippy

develop:
	maturin develop --release
	pytest -v

test:
	cargo test --lib

cover:
	cargo llvm-cov --html --open --ignore-filename-regex lib.rs

doc:
	cargo doc --open

sample:
	python py/sample.py data/evil_2.csv
