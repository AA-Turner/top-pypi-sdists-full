/*
 * Global defaults incl. a dark mode theme
 * Dark mode theme is automatically activated based on media query
 *
**/

'use strict';

// Shared defaults
const colors = {
	primary: '#375a7f',
	secondary: '#444444',
	success: '#00bc8c',
	info: '#3498db',
	warning: '#f39c12',
	danger: '#e74c3c',
	light: '#adb5bd',
	dark: '#303030',
	primary_2: '#375304',
	secondary_2: '#383838',
	success_2: '#0c8667',
	info_2: '#2e6f9a',
	warning_2: '#aa7118',
	danger_2: '#a23d33',
	light_2: '#7c8287',
	dark_2: '#2b2b2b',
}

Highcharts.theme = {
	credits: {
		enabled: false
	},
	colors: [
		colors.success,
		colors.primary,
		colors.danger,
		colors.warning,
		colors.secondary,
		colors.info,
		colors.light,
		colors.dark,
		colors.success_2,
		colors.primary_2,
		colors.danger_2,
		colors.warning_2,
		colors.secondary_2,
		colors.info_2,
		colors.light_2,
		colors.dark_2,
	],
}

const matchesDarkMode = window.matchMedia("(prefers-color-scheme: dark)");
if (matchesDarkMode.matches) {
	// Dark mode styling
	const normalTextColor = '#eeeeee'; //'#9F9F9F'
	const backgroundColor = '#121212';
	Object.assign(
		Highcharts.theme, {
		chart: {
			backgroundColor: backgroundColor,
			style: {
				fontFamily: 'Tahoma, Geneva, sans-serif'
			},
			plotBorderColor: '#606063'
		},
		title: {
			style: {
				color: '#E0E0E3',
				fontSize: "15px",
				fontWeight: "bold"
			}
		},
		subtitle: {
			style: {
				color: '#E0E0E3',
				textTransform: 'uppercase'
			}
		},
		xAxis: {
			gridLineColor: '#404040',
			labels: {
				style: {
					fontSize: "13px",
					color: normalTextColor
				}
			},
			lineColor: '#404040',
			minorGridLineColor: '#505053',
			tickColor: '#404040',
			tickWidth: 1,
			title: {
				style: {
					color: normalTextColor
				}
			}
		},
		yAxis: {
			gridLineColor: '#404040',
			labels: {
				style: {
					color: normalTextColor
				}
			},
			lineColor: '#404040',
			minorGridLineColor: '#505053',
			tickColor: '#404040',
			tickWidth: 1,
			title: {
				style: {
					color: normalTextColor
				}
			}
		},
		tooltip: {
			backgroundColor: 'rgba(0, 0, 0, 0.85)',
			style: {
				color: '#F0F0F0'
			}
		},
		plotOptions: {
			series: {
				dataLabels: {
					color: '#B0B0B3'
				},
				marker: {
					lineColor: '#333'
				}
			},
			bar: {
				animation: false,
				borderColor: backgroundColor,
				dataLabels: {
					format: "{y}",
					style: {
						fontSize: "13px"
					},
					enabled: true
				}
			},
			column: {
				animation: false,
				borderColor: backgroundColor,
			},
			line: {
				animation: false,
				lineWidth: 2,
				marker: {
					radius: 3
				}
			},
			pie: {
				animation: false,
				borderColor: backgroundColor
			},
			boxplot: {
				fillColor: '#505053'
			},
			candlestick: {
				lineColor: 'white'
			},
			errorbar: {
				color: 'white'
			}
		},
		legend: {
			borderColor: "#404040",
			itemStyle: {
				color: normalTextColor
			},
			itemHoverStyle: {
				color: '#FFF'
			},
			itemHiddenStyle: {
				color: '#606063'
			}
		},
		labels: {
			style: {
				color: '#707073'
			}
		},

		drilldown: {
			activeAxisLabelStyle: {
				color: '#F0F0F3'
			},
			activeDataLabelStyle: {
				color: '#F0F0F3'
			}
		},

		navigation: {
			buttonOptions: {
				symbolStroke: '#DDDDDD',
				theme: {
					fill: '#505053'
				}
			}
		},

		// scroll charts
		rangeSelector: {
			buttonTheme: {
				fill: '#505053',
				stroke: '#000000',
				style: {
					color: '#CCC'
				},
				states: {
					hover: {
						fill: '#707073',
						stroke: '#000000',
						style: {
							color: 'white'
						}
					},
					select: {
						fill: '#000003',
						stroke: '#000000',
						style: {
							color: 'white'
						}
					}
				}
			},
			inputBoxBorderColor: '#505053',
			inputStyle: {
				backgroundColor: '#333',
				color: 'silver'
			},
			labelStyle: {
				color: 'silver'
			}
		},

		navigator: {
			handles: {
				backgroundColor: '#666',
				borderColor: '#AAA'
			},
			outlineColor: '#CCC',
			maskFill: 'rgba(255,255,255,0.1)',
			series: {
				color: '#7798BF',
				lineColor: '#A6C7ED'
			},
			xAxis: {
				gridLineColor: '#505053'
			}
		},

		scrollbar: {
			barBackgroundColor: '#808083',
			barBorderColor: '#808083',
			buttonArrowColor: '#CCC',
			buttonBackgroundColor: '#606063',
			buttonBorderColor: '#606063',
			rifleColor: '#FFF',
			trackBackgroundColor: '#404043',
			trackBorderColor: '#404043'
		},

		// special colors for some of the
		legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
		background2: '#505053',
		dataLabelsColor: '#B0B0B3',
		textColor: '#C0C0C0',
		contrastTextColor: '#F0F0F3',
		maskColor: 'rgba(255,255,255,0.3)'
	});
}
else {
	// Light mode styling
	// Object.assign(
	// 	Highcharts.theme, {
	// 	colors: ['#18bc9c', '#2c3e5a', '#e74c3c', '#f39c12', '#95a5a6', '#3498db', '#ecf0f1', '#7b8a8b'],
	// });
}

// Apply the theme
Highcharts.setOptions(Highcharts.theme);
