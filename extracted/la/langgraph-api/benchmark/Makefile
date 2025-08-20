# Benchmark commands
benchmark-burst:
	make benchmark-reset
	k6 run burst.js

benchmark-ramp:
	make benchmark-reset
	k6 run --out json=raw_data_$(shell date +%Y-%m-%dT%H-%M-%S).json ramp.js

benchmark-charts:
	npm install
	node graphs.js $(shell ls -t raw_data_*.json | head -1) true

benchmark-reset:
	node clean.js

benchmark-new-revision:
	node update-revision.js

benchmark-clean:
	rm -f results_*.json summary_*.json raw_data_*.json *_chart_*.png

benchmark-clean-charts:
	rm -f *_chart_*.png