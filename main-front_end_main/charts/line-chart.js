google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Day');
    data.addColumn('number', 'Factors');


    data.addRows([

        [1, 10],
        [2, 15],
        [3, 4],
        [4, 23],
        [5, 10],
        [6, 4],
        [7, 11],
        [8, 5],
        [9, 5],
        [10, 5],
        [11, 11],
        [12, 13],
        [13, 17],
        [14, 20],
        [15, 21],
        [16, 20],
        [17, 23],
        [18, 25],
        [19, 24],
        [20, 12],
        [21, 12],
        [22, 10],
        [23, 13],
        [24, 16],
        [25, 17],
        [26, 8],
        [27, 5],
        [28, 7],
        [29, 15],
        [30, 20],
        [31, 17]
    ]);

    var options = {
        chart: {
            title: 'Total stats',
            subtitle: 'out of 25'
        },vAxis: {
        scaleType: 'log'
  },
        axes: {
            x: {
                all: {
                    range: {
                        max: 31,
                        min: 1
                    }
                }
            }
        },
        width: 900,
        height: 500
    };

    var chart = new google.charts.Line(document.getElementById('line_div'));

    chart.draw(data, options);
}
