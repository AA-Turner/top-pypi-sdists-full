const fs = require('fs');
const path = require('path');
const readline = require('readline');
const QuickChart = require('quickchart-js');
const { plot } = require('nodeplotlib');

// Function to save chart using Quickchart
async function saveChartWithQuickchart(chartData, chartLayout, filename) {
  const chart = new QuickChart();

  chart.setWidth(800);
  chart.setHeight(500);
  chart.setFormat('png');

  const config = {
    type: 'line',
    data: {
      labels: chartData[0].x,
      datasets: chartData.map(metric => {
        return {
            label: metric.name,
            data: metric.y
        }
      })
    }
  };

  chart.setConfig(config);

  try {
    const imageBuffer = await chart.toBinary();
    fs.writeFileSync(filename, imageBuffer);
    console.log(`Chart saved to ${filename}`);
  } catch (error) {
    console.error(`Error saving chart to ${filename}:`, error.message);
  }
}

/**
 * Function to generate charts from benchmark results
 * 
 * Graphs that we generate:
 * - VU scaling over time
 * - Requests over time, broken into success and failure by reason
 * - Average run duration over time
 * 
 * Useful but currently in deployment dashboard:
 * - Connection use over time (postgres, redis)
 * - IOPS over time (postgres, redis)
 * - Workers in use over time
 * 
 * Dashboard: https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/host/deployments/a23f03ff-6d4d-4efd-8149-bb5a7f3b95cf?tab=2&paginationModel=%7B%22pageIndex%22%3A0%2C%22pageSize%22%3A10%7D#
 */
async function generateCharts(rawDataFile, displayInBrowser = false) {
    console.log("Generating charts for", rawDataFile);
    const aggregatedData = {};

    // Read the results and summary files
    const fileStream = fs.createReadStream(rawDataFile, 'utf8');
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        const entry = JSON.parse(line);

        // Always written before the first point for that metric
        if (entry.type === 'Metric') {
            const metricName = entry.metric;
            aggregatedData[metricName] = {};
        } else if (entry.type === 'Point') {
            const metricName = entry.metric;
            const metricValue = entry.data.value;
            const timestamp = Date.parse(entry.data.time);

            // Round timestamp to 10-second intervals
            const roundedTimestamp = Math.floor(timestamp / 10000) * 10000;

            if (!aggregatedData[metricName][roundedTimestamp]) {
                aggregatedData[metricName][roundedTimestamp] = [];
            }
            aggregatedData[metricName][roundedTimestamp].push(metricValue);
        } else {
            throw new Error(`Unexpected row type: ${entry.type}`);
        }
    }

    // Convert aggregated data to final format with averages
    const finalData = {};
    for (const [metricName, timestampBuckets] of Object.entries(aggregatedData)) {
        finalData[metricName] = [];
        for (const [timestamp, values] of Object.entries(timestampBuckets)) {
            const average = values.reduce((sum, val) => sum + val, 0) / values.length;
            const max = Math.max(...values);
            finalData[metricName].push({ 
                timestamp: timestamp,
                average: average,
                max: max,
                count: values.length
            });
        }
        // Sort by timestamp
        finalData[metricName].sort((a, b) => a.timestamp - b.timestamp);
    }

    // Create the charts
    // We always get a http_reqs metric as one of the first
    const firstTimestamp = finalData['http_reqs'][0].timestamp;

    // Failed requests won't always be present
    const data = [
        {
            x: finalData['http_reqs'].map(d => (d.timestamp - firstTimestamp) / 1000),
            y: finalData['http_reqs'].map(d => d.count),
            type: 'scatter',
            mode: 'lines',
            name: 'Total Requests',
        },
        {
            x: finalData['successful_runs'].map(d => (d.timestamp - firstTimestamp) / 1000),
            y: finalData['successful_runs'].map(d => d.count),
            type: 'scatter',
            mode: 'lines',
            name: 'Success Rate',
        }
    ]
    if (finalData['failed_runs']) {
        data.push({
            x: finalData['failed_runs'].map(d => (d.timestamp - firstTimestamp) / 1000),
            y: finalData['failed_runs'].map(d => d.count),
            type: 'scatter',
            mode: 'lines',
            name: 'Failed Requests',
        })
    }

    const requestsChart = {
        data,
        layout: {
        title: {
            text: 'Success Rate Over Time',
        },
        xaxis: { 
            title: 'Time (10 second intervals)',
        },
        yaxis: { 
            title: 'Call Counts',
        }
        }
    };

    const runDurationChart = {
        data: [
        {
            x: finalData['run_duration'].map(d => (d.timestamp - firstTimestamp) / 1000),
            y: finalData['run_duration'].map(d => d.average),
            type: 'scatter',
            mode: 'lines',
            name: 'Run Duration',
        }
        ],
        layout: {
        title: {
            text: 'Run Duration Over Time',
        },
        xaxis: { 
            title: 'Time (10 second intervals)',
        },
        yaxis: { 
            title: 'Run Duration (ms)',
        },
        }
    }

    const vusChart = {
        data: [
        {
            x: finalData['vus'].map(d => (d.timestamp - firstTimestamp) / 1000),
            y: finalData['vus'].map(d => d.max),
            type: 'scatter',
            mode: 'lines',
            name: 'Concurrent Virtual Users',
        }
        ],
        layout: {
        title: {
            text: 'Concurrent Virtual Users over Time',
        },
        xaxis: { 
            title: 'Time (10 second intervals)',
        },
        yaxis: { 
            title: 'VUs (max)',
        },
        }
    }

    // Always save charts as images using Quickchart
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const requestsImagePath = path.join(__dirname, `requests_chart_${timestamp}.png`);
    const runDurationImagePath = path.join(__dirname, `run_duration_chart_${timestamp}.png`);
    const vusImagePath = path.join(__dirname, `vus_chart_${timestamp}.png`);

    // Save charts using Quickchart
    await saveChartWithQuickchart(requestsChart.data, requestsChart.layout, requestsImagePath);
    await saveChartWithQuickchart(runDurationChart.data, runDurationChart.layout, runDurationImagePath);
    await saveChartWithQuickchart(vusChart.data, vusChart.layout, vusImagePath);

    // Display in CLI if requested
    if (displayInBrowser) {
        plot(requestsChart.data, requestsChart.layout);
        plot(runDurationChart.data, runDurationChart.layout);
        plot(vusChart.data, vusChart.layout);
    }
    
    console.log(`Charts generated: ${vusImagePath}, ${requestsImagePath}, ${runDurationImagePath}`);
}

// CLI usage
if (require.main === module) {
  const [,, rawDataFile, displayInBrowser] = process.argv;
  
  if (!rawDataFile) {
    console.error('Usage: node graphs.js <raw-data-file>');
    process.exit(1);
  }
  
  generateCharts(rawDataFile, displayInBrowser)
    .catch(error => {
      console.error('Failed to generate charts:', error);
      process.exit(1);
    });
}

module.exports = { generateCharts };
