$( function() {
                $( "#slider-range" ).slider({
                range: true,
                min: 1,
                max: 7,
                values: [ 1,7 ],

                slide: function( event, ui ) {
                    $( "#amount" ).val(  ui.values[ 0 ] + ". - " + ui.values[ 1 ]  + ". of December");
                    $("#from_day").val(ui.values[ 0 ]);
                    $("#to_day").val(ui.values[ 1 ]);
                }
                });
                $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
                ". - " + $( "#slider-range" ).slider( "values", 1 ) + ". of December");
                $("#from_day").val($( "#slider-range" ).slider( "values", 0 ));
                $("#to_day").val($( "#slider-range" ).slider( "values", 1 ))
            });