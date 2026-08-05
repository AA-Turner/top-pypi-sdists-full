# Benchmark commands

benchmark-ramp:
	make benchmark-reset
	npm install
	npm run build
	k6 run --out json=raw_data_$(shell date +%Y-%m-%dT%H-%M-%S).json --system-tags=[] ramp.js

benchmark-charts:
	npm install
	node graphs.js $(shell ls -t raw_data_*.json | head -1) true

benchmark-reset:
	node clean-cli.js

benchmark-new-revision:
	node update-revision.js

benchmark-staircase:
	python staircase.py

benchmark-staircase-reset:
	python ../../scripts/reset_deployment.py -a $(BENCHMARK_APP_NAME) -n $(BENCHMARK_NAMESPACE) -db $(BENCHMARK_DB_INSTANCE)
	python staircase.py

benchmark-clean:
	rm -f results_*.json summary_*.json raw_data_*.json staircase_*.json *_chart_*.png

benchmark-clean-charts:
	rm -f *_chart_*.png
