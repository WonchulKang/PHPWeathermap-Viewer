
refresh_timer = null;
refresh_timer = setInterval(start_up, 30000);

function view_close() {
	$("#float").addClass("hidden");
	$("#graph_img").attr("src", "");
}

function view_graph(base_url, id) {
	$("#graph_img").attr("src", base_url + id);
	$("#float").removeClass("hidden");
}

function start_up() {
	update_year();
	$.ajax( {
		url	: "/data/image",
		type	: "GET",
		success	: function(result) {
			update_main(result['filename'], result['prev'], null);
		},
		error	: function() {
			alert("파일 위치 읽기에 실패하였습니다.");
		}
	});
}

function reset() {
	start_up();
}

function refresh_call() {
	if(refresh_timer != null) {
		clearInterval(refresh_timer);
		refresh_timer = null;
		$("#refresh_button").val("REFRESH ON");
	} else {
		refresh_timer = setInterval(start_up, 30000);
		$("#refresh_button").val("REFRESH OFF");
	}
}

function update_image(year, month, day, hour, min) {
	param = { "year" : String(year),
		  "month" : String(month),
		  "day" : String(day),
		  "hour" : String(hour),
		  "min" : String(min) };
	$.ajax( {
		url	: "/data/image",
		type	: "GET",
		data	: param,
		success : function(result) {
			update_main(result['filename'], result['prev'], null);
		},
		error	: function() {
			alert("이미지 업데이트에 실패하였습니다.");
		}
	});
}

function update_main(file_name, prev, next) {
	$("#view").attr("src", file_name);
	var split_string = file_name.split("/");
	var time_info = split_string[split_string.length - 1].split("+")[0].replace("T", " ");
	$("#c_time").text(time_info);

	if (prev != null ) {
		$("#prev_link").attr("href", "javascript:update_image('" + prev.year + "', '" +
								           prev.month + "', '" +
									   prev.day + "', '" +
									   prev.hour + "', '" +
			                                                   prev.minute + "');");
		clearInterval(refresh_timer);
		refresh_timer = null;
	} else {
		$("#prev_link").attr("href", "javascript:alert('이전 데이터가 없습니다.');");
	}
}

function update_year() {
	$("#year_select").unbind();
	$("#year_select option[value!='-']").each(function() {
		$(this).remove();
	});
	update_month("-");
	$.ajax( {
		url	: "/data",
		type	: "GET",
		success : function(result) {
			$.each(result['year'], function(index, item) {
				$("#year_select").append($("<option>", 
					                 { "value" : item, "class" : "year" }).text(item));
			});
		},
		error	: function() {
			alert("년도 정보 읽기를 실패하였습니다.");
		}
	});
	$("#year_select").on("change", function() {
		update_month($(this).val());
	});
}

function update_month(year) {
	$("#month_select").unbind();
	$("#month_select option[value!='-']").each(function() {
		$(this).remove();
	});
	update_day(year, "-");
	if(year != "-") {
		$.ajax( {
			url	: "/data/" + year,
			type	: "GET",
			success : function(result) {
				$.each(result['month'], function(index, item) {
					$("#month_select").append($("<option>", 
						                  { "value" : item, "class" : "month" }).text(item));
				});
			},
			error	: function() {
				alert("월 정보 읽기를 실패하였습니다.");
			}
		});
	}
	$("#month_select").on("change", function() {
		update_day(year, $(this).val());
	});
}

function update_day(year, month) {
	$("#day_select").unbind();
	$("#day_select option[value!='-']").each(function() {
		$(this).remove();
	});
	update_hour(year, month, "-");
	if(year != "-" && month != "-") {
		$.ajax( {
			url	: "/data/" + year + "/" + month,
			type	: "GET",
			success : function(result) {
				$.each(result['day'], function(index, item) {
					$("#day_select").append($("<option>", 
						                  { "value" : item, "class" : "day" }).text(item));
				});
			},
			error	: function() {
				alert("일 정보 읽기를 실패하였습니다.");
			}
		});
	}
	$("#day_select").on("change", function() {
		update_hour(year, month, $(this).val());
	});
}

function update_hour(year, month, day) {
	$("#hour_select").unbind();
	$("#hour_select option[value!='-']").each(function() {
		$(this).remove();
	});
	update_min(year, month, day, '-');
	if(year != "-" && month != "-" && day != "-") {
		$.ajax( {
			url	: "/data/" + year + "/" + month + "/" + day,
			type	: "GET",
			success : function(result) {
				$.each(result['hour'], function(index, item) {
					$("#hour_select").append($("<option>", 
						                  { "value" : item, "class" : "hour" }).text(item));
				});
			},
			error	: function() {
				alert("시 정보 읽기를 실패하였습니다.");
			}
		});
	}
	$("#hour_select").on("change", function() {
		update_min(year, month, day, $(this).val());
	});
}

function update_min(year, month, day, hour) {
	$("#min_select").unbind();
	$("#min_select option[value!='-']").each(function() {
		$(this).remove();
	});
	if(year != "-" && month != "-" && day != "-" && hour != '-') {
		$.ajax( {
			url	: "/data/" + year + "/" + month + "/" + day + "/" + hour,
			type	: "GET",
			success : function(result) {
				$.each(result['minute'], function(index, item) {
					$("#min_select").append($("<option>", 
						                  { "value" : item, "class" : "min" }).text(item));
				});
			},
			error	: function() {
				alert("분 정보 읽기를 실패하였습니다.");
			}
		});
	}
	$("#min_select").on("change", function() {
		update_image(year, month, day, hour, $(this).val());
	});
	clearInterval(refresh_timer);
	refresh_timer = null;
}
