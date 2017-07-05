var time_loaded;

voi_ptrs = {
1 :["dolnośląskie"],
2 :["kujawsko-pomorskie"],
3 :["lubelskie"],
4 :["lubuskie"],
5 :["łódzkie"],
6 :["małopolskie"],
7 :["mazowieckie"],
8 :["opolskie"],
9 :["podkarpackie"],
10 :["podlaskie"],
11 :["pomorskie"],
12 :["śląskie"],
13 :["świętokrzystkie"],
14 :["warmińsko-mazurskie"],
15 :["wielkopolskie"],
16 :["zachodniopomorskie"]
}

kinds = {
1: ["miasto"],
2: ["wieś"],
3: ["statki"],
4: ["zagranica"]
}

function add_row(vote, comm, voi_nr) {

    var percent_1 = 100 * vote.votes_for_cand_1 / (vote.votes_for_cand_1 + vote.votes_for_cand_2);
    var percent_2 = 100 - percent_1;

    var row = " <tr><td>" + comm.name + " gm.</td> \
                <td>" + kinds[comm.kind] + "</td> \
                <td>" + voi_ptrs[voi_nr] + " woj.</td> \
                <td>" + vote.valid_votes + "</td> \
                <td>" + vote.votes_for_cand_1 + "</td> \
                <td>" + percent_1.toFixed(2) + "</td> \
                <td> \
                    <div class=\"progressbar\"> \
                        <div style=\"width:" + percent_1 + "%\"></div> \
                    </div> \
                </td> \
                <td>" + percent_2.toFixed(2) + "</td> \
                <td>" + vote.votes_for_cand_2 + "</td> \
                <td style=\"background-color:transparent; color:black\"> \
                <span id=\"" + comm.name + "\" class=\"w3-btn\" onclick=\"document.getElementById('modal2').style.display='block'; prepare_form('" + comm.name + 
                "')\" style=\"background-color:transparent; color:black\">modyfikuj</span> \
                </td> \
                </tr> "
    $("#tbody").append(row);
}

function prepare_form(comm_name) {
    $("#modal2").attr("data-name",  comm_name);
    // $("#modal2").attr("data-date", comm_last_mod);
    $("form").trigger("reset");
    // console.log(comm_last_mod);
}

function find_vote_object(votes, comm) {
    for (v = 0; v < votes.length; v++) {
        if (votes[v].community_ptr == comm.name)
            var vote = votes[v];
    };
    return vote;
}

$(document).ready(function() {

    time_loaded = new Date().getTime();
    $('.voi_name, .area_type, .dist_amount').click(function() {
        var clicked = $(this);

        $("#tbody").empty();

        // AJAX call
        $.get('/elections/ajax_get/', function(data) {
            var jsonData = $.parseJSON(data);
            var comms = jsonData.communities;
            var votes = jsonData.votes;

            if (clicked.hasClass('voi_name')) {
                var v_name = clicked.attr("id");
                for (d = 0; d < comms.length; d++) {
                    var vote = find_vote_object(votes, comms[d]);
                    var voi_nr = comms[d].voivodeship_ptr;

                    if (voi_ptrs[voi_nr][0] == v_name) {
                        add_row(vote, comms[d], voi_nr);
                    };
                };
            } else if (clicked.hasClass('area_type')) {
                var type = clicked.attr("id").toLowerCase();
                for (d = 0; d < comms.length; d++) {
                    var vote = find_vote_object(votes, comms[d]);
                    var kind_nr = comms[d].kind;
                    var voi_nr = comms[d].voivodeship_ptr;

                    if (kinds[kind_nr][0] == type) {
                        add_row(vote, comms[d], voi_nr);
                    };
                };
            } else if (clicked.hasClass('dist_amount')) {
                var min = clicked.attr("data-min");
                var max = clicked.attr("data-max");

                for (d = 0; d < comms.length; d++) {
                    var vote = find_vote_object(votes, comms[d]);
                    var voi_nr = comms[d].voivodeship_ptr;

                    if (comms[d].citizens > min && comms[d].citizens < max) {
                        add_row(vote, comms[d], voi_nr);
                    };
                };
            };
        });

    });

    //For getting CSRF token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
    return cookieValue;
    }

    //For doing AJAX post

    //When submit is clicked

    // $('.community').click(function() {

    //     var name = $(this).attr("id");
        
    // });    

    $("#submit").click(function(e) {

        //Prevent default submit. Must for Ajax post.Beginner's pit.
        e.preventDefault();


        //Prepare csrf token
        var csrftoken = getCookie('csrftoken');


        //Collect data from fields
        var name = $('#modal2').attr("data-name");
        var mod_date = new Date($('#modal2').attr("data-date"));
        var voting_cards = $('#inputVotingCards').val();
        var votes = $('#inputVotes').val();
        var valid_votes = $('#inputValidVotes').val();
        var votes_for_cand_1 = $('#inputVotesForCand1').val();
        var votes_for_cand_2 = $('#inputVotesForCand2').val();

         /* checking if the value has changed since loading the page */
        $.ajax({
            url : "get_last_modification/", // the endpoint,commonly same url
            type : "POST", // http method
            data : { csrfmiddlewaretoken : csrftoken,
            community_name : name,
            }, // data sent with the post request

            success : function(json) {
                var last_modification = json['last_modification'];
                last_modification = Date.parse(last_modification);
                console.log(time_loaded);
                console.log(last_modification);

                if (time_loaded < last_modification) {
                    var msg = "Wyglada na to, że ktos edytowal dane dotyczące tej gminy, " +
                        "gdy byłes już zalogowany. Odswiez strone i sprobuj ponownie";
                    alert(msg);
                    document.getElementById("not-edited").attr(data-msg) = msg;
                } else {
                    //Send data  
                    $.ajax({
                        url : "update_vote/", // the endpoint,commonly same url
                        type : "POST", // http method
                        data : { csrfmiddlewaretoken : csrftoken, 
                        name : name,
                        mod_date : mod_date.toJSON(),
                        voting_cards : voting_cards,
                        votes : votes,
                        valid_votes : valid_votes,
                        votes_for_cand_1 : votes_for_cand_1,
                        votes_for_cand_2 : votes_for_cand_2,
                        }, // data sent with the post request

                        // handle a successful response
                        success : function(json) {
                            if (json['ret_val'] != 0) {
                                alert(json['ret']);
                            // } else {
                                // confirm("Czy na pewno chcesz nadpisać dane?");
                            }
                        },

                        // handle a non-successful response
                        error : function(xhr,errmsg,err) {
                            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                        }
                    });
                }
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
        });
    });
});