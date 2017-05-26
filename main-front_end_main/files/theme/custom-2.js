function main() {
    google.charts.load("43", {packages: ["corechart", "gauge", "table", "timeline", "bar"]});
    google.charts.setOnLoadCallback(drawChart);
    function addingRowsManually(firstDate, amount, content, data) {
        // console.log(content);
        var changingList;
        var changingDate;
        var firstDateList = firstDate.split('-');
        // console.log(firstDateList);
        var customDate = new Date(firstDateList[0], parseInt(firstDateList[1]) - 1, firstDateList[2]);
        //console.log(customDate);
        //console.log(customDate.getDate());
        for (var i = customDate.getDate() - amount; i <= customDate.getDate(); i++){
            changingDate = new Date(firstDateList[0], parseInt(firstDateList[1]) - 1, i);
            changingList = [changingDate.getDate().toString()];
            var changingDateStr = changingDate.getFullYear().toString();
            if (changingDate.getMonth() <= 8){
                changingDateStr += '-0' + (changingDate.getMonth() + 1);
            }
            else {
                changingDateStr += '-' + changingDate.getMonth();
            }
            if (changingDate.getDate() <= 9){
                changingDateStr += '-0' + changingDate.getDate();
            }
            else {
                changingDateStr += '-' + changingDate.getDate();
            }
            // console.log(changingDateStr);
            // console.log(changingDateStr);
            changingList.push.apply(changingList, content[changingDateStr][0]);
            //console.log(changingDateStr);
            //console.log(changingList);
            data.addRow(changingList);
        }
    }
    // console.log(myVariable['2017-04-01']);
    function drawChart() {
        var data = new google.visualization.DataTable;
        data.addColumn('string', 'Date');
        data.addColumn('number', 'вологість');
        data.addColumn('number', 'атмосферний тиск');
        data.addColumn('number', 'опади');
        //for (var i = 8; i <= 30; i++){
        //    data.addRow([i.toString(), Math.floor((Math.random() * 10)), Math.floor((Math.random() * 10)), Math.floor((Math.random() * 10))]);
        //}
        $.getJSON('info.json', function (datas) {
          // console.log(datas["2017-04-15"][0]);
          // data.addRow(["adD", 1, 2, 3]);
          addingRowsManually("2017-04-15", 28, datas, data);
        });
        var options = {
            chart: {
                title: 'Статистика за останні 28 днів',
                subtitle: 'фактори: вологість, атмосферний тиск, опади'
            },
            bars: 'vertical',
            vAxis: {format: 'decimal'},
            height: '100%',
            width: '50%',
            colors: ['#1b9e77', '#d95f02', '#7570b3'],
            allowHtml: true
        };

        var container = document.getElementById('custom_window_sec');

        container.style.display = 'block';

        var chart = new google.charts.Bar(document.getElementById('custom_window_three'));

        google.visualization.events.addListener(chart, 'ready', function () {
            container.style.display = 'none';
            $('#custom_window svg').css('width', '1100px');
            });

        chart.draw(data, options);
    }


    function calculate_date(zm) {
        var today = new Date();
        var dd = today.getDate() + zm;
        var mm = today.getMonth() + 1; //January is 0!
        var yyyy = today.getFullYear();
        if (dd < 10) {
            dd = '0' + dd
        }
        if (mm < 10) {
            mm = '0' + mm
        }
        return yyyy + '-' + mm + '-' + dd;
    }
    function bindImages(data_spec){
        return function () {
               $(window).hide();
                // console.log(a);
                // console.log(data[a][3][0]);
                // console.log(data[a][3][1]);
            var table_text = '<tr><td rowspan="'+ data_spec[0].length+  '" style="font-weight: bold;">Основні фактори: </td>';
            // console.log(data['2017-04-' + startPoint][3][1][0].join('<br>') + '</td></tr>');
            for (var i = 0; i < data_spec[0].length; i++){
                if (i == 0) {
                    table_text += '<td>' + data_spec[0][i] + '</td></tr>'
                }
                else {
                    table_text += '<tr><td>' + data_spec[0][i] + '</td></tr>'
                }
            }
            table_text +='<tr><td rowspan="'+ data_spec[1].length + '" style="font-weight: bold; border-bottom: 0;">Групи ризику: </td>';

            for (var i = 0; i < data_spec[1].length; i++){
                if (i == 0) {
                    table_text += '<td>' + data_spec[1][i].join('<br>') + '</td></tr>'
                }
                else {
                    table_text += '<tr><td>' + data_spec[1][i].join('<br>') + '</td></tr>'
                }
            }
            // console.log(12345);
            // console.log(table_text);
            $('#custom_window tbody').html(table_text);

                // $('#text3').text("Основні фактори: " + data_spec[0]);
                // $('#text4').text("Група максимального впливу: " + data_spec[1]);
                $(window).slideToggle(500);
        }
    }
    var weekday = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"];
    function getDayName(Date_a) {
        var splitted_date = Date_a.split('-');
        var d = new Date(parseInt(splitted_date[0]), parseInt(splitted_date[1]) - 1, parseInt(splitted_date[2]));
        return weekday[d.getDay()];
    }
    var startPoint = 15;
    var startPointStr;
    if (startPoint < 10) {
        startPointStr = '0' + startPoint;
    }
    else {
        startPointStr = startPoint.toString();
    }
    var window = document.getElementById('custom_window');
    $.getJSON('info.json', {}, function (data) {
        // console.log(data);
    // $.getJSON('https://medicasts.herokuapp.com/data.json', {}, function (data) {
       var table_text = '<tr><td rowspan="'+ data['2017-04-' + startPointStr][3][0].length+  '" style="font-weight: bold;">Основні фактори: </td>';
        // console.log(data['2017-04-' + startPoint][3][1][0].join('<br>') + '</td></tr>');
        for (var i = 0; i < data['2017-04-' + startPointStr][3][0].length; i++){
            if (i == 0) {
                table_text += '<td>' + data['2017-04-' + startPointStr][3][0][i] + '</td></tr>'
            }
            else {
                table_text += '<tr><td>' + data['2017-04-' + startPointStr][3][0][i] + '</td></tr>'
            }
        }
        table_text +='<tr><td rowspan="'+ data['2017-04-' + startPointStr][3][1].length + '" style="font-weight: bold; border-bottom: 0;">Групи ризику: </td>';

        for (var i = 0; i < data['2017-04-' + startPointStr][3][1].length; i++){
            if (i == 0) {
                table_text += '<td>' + data['2017-04-' + startPointStr][3][1][i].join('<br>') + '</td></tr>'
            }
            else {
                table_text += '<tr><td>' + data['2017-04-' + startPointStr][3][1][i].join('<br>') + '</td></tr>'
            }
        }
        // console.log(12345);
        $('#day_block tbody').append(table_text);

        $('#day_text').text(data['2017-04-' + startPointStr][1].toString() + ' тип небезпеки');
        for (var i = 0; i <= 6; i++) {
            if (startPoint + i <= 9) {a = '2017-04-0' + (startPoint + i).toString()}
            else{
            a = '2017-04-' + (startPoint + i).toString();
            // console.log(a);
            }
            // console.log(getDayName(a));
            if (i > 0) {
                $('#Table_Days tr td:nth-child(' + i.toString() + ')').text(getDayName(a));
            }
            $('div#Photo' + (i + 1) + ' > a > img').attr('src', './levels/' + data[a][1].toString() + '.png');
            $('div#Photo' + (i + 1).toString()).on('click', bindImages(data[a][3]));
        }
        });
    // console.log(new Date(2017, 1, -5));
    var elmntSec = document.getElementById("custom_window_sec");
    $('#show_graph').on('click', function () {
        $('#custom_window_sec').slideToggle(500);
        elmntSec.scrollIntoView();
        });
}
$(document).ready(main);
