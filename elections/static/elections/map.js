    google.load("visualization", "1", {packages: ["geochart"]});
    google.setOnLoadCallback(drawRegionsMap);

    function drawRegionsMap() {

        var data = google.visualization.arrayToDataTable(geo_data_1);
        var data2 = google.visualization.arrayToDataTable(geo_data_2);

        var options = {
            region: 'PL',
            resolution: 'provinces',
            colorAxis: {
                colors: ['#f0d37e', 'orange']
            },
            backgroundColor: '#81d4fa',
            datalessRegionColor: '#ffffff',
            defaultColor: '#f5f5f5',
            width: '400',
            keepAspectRatio: 'True'

        };

        var options_2 = {
            region: 'PL',
            resolution: 'provinces',
            colorAxis: {
                colors: ['#7eb9f0', '#0e7de3']
            },
            backgroundColor: '#81d4fa',
            datalessRegionColor: '#ffffff',
            defaultColor: '#f5f5f5',
            width: '400',
            keepAspectRatio: 'True'

        };

        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
        var chart_2 = new google.visualization.GeoChart(document.getElementById('regions_div_2'));

        chart.draw(data, options);
        chart_2.draw(data2, options_2);
    }