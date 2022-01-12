



// Combined info from two tutorials: 
// https://www.d3-graph-gallery.com/graph/barplot_button_data_hard.html
// https://www.d3-graph-gallery.com/graph/barplot_horizontal.html




var num_chars = 20


//LOAD JSON DATA and create data structures as appropriate

data_all = []
data_1 = []
data_2 = []
data_3 = []
data_4 = []
data_5 = []
data_6 = []
data_7 = []
data_8 = []

//Read the data
d3.json("data/all_char_word_counts.json", function(json_data) {

	
	//CALCULATE ALL SEASONS
	json_data = json_data.sort(function(a,b){ return b.word_tot - a.word_tot; });
	for (let i = 0; i < num_chars; i++) {
		data_all.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['word_tot']
		});
	}
	data_all = data_all.reverse()

	//CALCULATE SEASON 1
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[0] - a.season_word_tots[0]; });
	for (let i = 0; i < num_chars; i++) {
		data_1.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][0]
		});
	}
	data_1 = data_1.reverse()

	//CALCULATE SEASON 2
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[1] - a.season_word_tots[1]; });
	for (let i = 0; i < num_chars; i++) {
		data_2.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][1]
		});
	}
	data_2 = data_2.reverse()

	//CALCULATE SEASON 3
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[2] - a.season_word_tots[2]; });
	for (let i = 0; i < num_chars; i++) {
		data_3.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][2]
		});
	}
	data_3 = data_3.reverse()

	//CALCULATE SEASON 4
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[3] - a.season_word_tots[3]; });
	for (let i = 0; i < num_chars; i++) {
		data_4.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][3]
		});
	}
	data_4 = data_4.reverse()

	//CALCULATE SEASON 5
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[4] - a.season_word_tots[4]; });
	for (let i = 0; i < num_chars; i++) {
		data_5.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][4]
		});
	}
	data_5 = data_5.reverse()

	//CALCULATE SEASON 6
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[5] - a.season_word_tots[5]; });
	for (let i = 0; i < num_chars; i++) {
		data_6.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][5]
		});
	}
	data_6 = data_6.reverse()

	//CALCULATE SEASON 7
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[6] - a.season_word_tots[6]; });
	for (let i = 0; i < num_chars; i++) {
		data_7.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][6]
		});
	}
	data_7 = data_7.reverse()

	//CALCULATE SEASON 8
	json_data = json_data.sort(function(a,b){ return b.season_word_tots[7] - a.season_word_tots[7]; });
	for (let i = 0; i < num_chars; i++) {
		data_8.push({
			'name': json_data[i]['name'],
			'word_tot': json_data[i]['season_word_tots'][7]
		});
	}
	data_8 = data_8.reverse()
	
})









//NOW COMBINE the different tutorials

// set the dimensions and margins of the graph
var margin = {top: 30, right: 30, bottom: 70, left: 120},
width = 800 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#word_char_chart")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// // Initialize the X axis
// var x = d3.scaleBand()
// 	.range([ 0, width ])
// 	.padding(0.2);
// var xAxis = svg.append("g")
// 	.attr("transform", "translate(0," + height + ")")

// Initialize the X axis
var x = d3.scaleLinear()
	.range([ 0, width ])
var xAxis = svg.append("g")
	.attr("transform", "translate(0," + height + ")")


// // Initialize the Y axis
// var y = d3.scaleLinear()
// 	.range([ height, 0]);
// var yAxis = svg.append("g")
// 	.attr("class", "myYaxis")

var y = d3.scaleBand()
	.range([ height, 0])
	.padding(0.2);
var yAxis = svg.append("g")
	.attr("class", "myYaxis");




// A function that create / update the plot for a given variable:
function update(data) {


	// // Update the X axis
	// x.domain(data.map(function(d) { return d.name; }))
	// xAxis.call(d3.axisBottom(x))

	// Update the X axis
	x.domain([0, d3.max(data, function(d) { return d.word_tot }) ]);
	xAxis.transition().duration(1000).call(d3.axisBottom(x));

	// // Update the Y axis
	// y.domain([0, d3.max(data, function(d) { return d.word_tot }) ]);
	// yAxis.transition().duration(1000).call(d3.axisLeft(y));

	// Update the Y axis
	y.domain(data.map(function(d) { return d.name; }));
	yAxis.call(d3.axisLeft(y));


	// Create the u variable
	var u = svg.selectAll("rect")
		.data(data);

	u
		.enter()
		.append("rect") // Add a new rect for each new elements
		.merge(u) // get the already existing elements as well
		.transition() // and apply changes to all of them
		.duration(1000)
		//.attr("x", function(d) { return x(d.name); })
		//.attr("y", function(d) { return y(d.word_tot); })
		//.attr("width", x.bandwidth())
		//.attr("height", function(d) { return height - y(d.word_tot); })
		.attr("x", x(0))
		.attr("y", function(d) {return y(d.name); })
		.attr("width", function(d) {return x(d.word_tot); })
		.attr("height", y.bandwidth())
		.attr("fill", "#69b3a2");

	// If less group in the new dataset, I delete the ones not in use anymore
	u
		.exit()
		.remove();

	// var t = svg.selectAll("text.bar")
	// 	.data(data)

	// t
 //        .enter()
 //        .append("text")
 //        .merge(t)
 //        .transition()
 //        .duration(1000)
 //        .attr("class", "yAxis-label")
 //        .attr("text-anchor", "middle")
 //        .attr("fill", "#70747a")
 //        .attr("x", function(d) {return x(d.word_tot); })
 //        .attr("y", function(d) {return y(d.name); })
 //        .text(d => d.word_tot);

 //    t
 //    	.exit()
 //    	.remove()

};






// Initialize the plot with the first dataset
update(data_1);
console.log("trying");
update(data_all);



