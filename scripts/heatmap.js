
//https://www.d3-graph-gallery.com/graph/heatmap_style.html
//https://www.d3-graph-gallery.com/graph/heatmap_tooltip.html



// set the dimensions and margins of the graph
var margin = {top: 60, right: 30, bottom: 150, left: 150},
	width = 800 - margin.left - margin.right,
	height = 750 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#heatmap_chart")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Labels of row and columns
//var myGroups = ["A", "B", "C", "D", "E"]
//var myVars = ["A", "B", "C", "D", "E"]
var myGroups = ['Arya Stark','Brienne of Tarth','Bronn','Cersei Lannister','Daenerys Targaryen','Davos Seaworth','Jaime Lannister','Jon Snow','Jorah Mormont','Lord Varys','Olenna Tyrell','Petyr Baelish','Robb Stark','Samwell Tarly','Sandor Clegane','Sansa Stark','Stannis Baratheon','Theon Greyjoy','Tyrion Lannister','Tywin Lannister']
var myVars = ['Arya Stark','Brienne of Tarth','Bronn','Cersei Lannister','Daenerys Targaryen','Davos Seaworth','Jaime Lannister','Jon Snow','Jorah Mormont','Lord Varys','Olenna Tyrell','Petyr Baelish','Robb Stark','Samwell Tarly','Sandor Clegane','Sansa Stark','Stannis Baratheon','Theon Greyjoy','Tyrion Lannister','Tywin Lannister']

// // Build X scales and axis:
// var x = d3.scaleBand()
// 	.range([ 0, width ])
// 	.domain(myGroups)
// 	.padding(0.01);
// svg.append("g")
// 	.style("font-size", 15)
// 	.attr("transform", "translate(0," + height + ")")
// 	.call(d3.axisBottom(x).tickSize(0))
// 	//.attr("transform", "rotate(-65)")
// 	.select(".domain").remove()

// Build X scales and axis:
var x = d3.scaleBand()
    .range([0, width])
    .domain(myGroups)
    .padding(0.01);
svg.append("g")
    .style("font-size", 15)
    .call(d3.axisRight(x).tickSize(0))
    .attr("transform", function(d, i) { return "translate(0,680)" + "rotate(-90)"})
    .select(".domain").remove()

// Build Y scales and axis:
var y = d3.scaleBand()
	.range([ height, 0 ])
	.domain(myVars)
	.padding(0.01);
svg.append("g")
	.style("font-size", 15)
	.call(d3.axisLeft(y).tickSize(0))
	.select(".domain").remove()

// Build color scale
var myColor = d3.scaleLinear()
	.range(["white", "#69b3a2"])
	.domain([1,50])

//Read the data
d3.csv("data/scene_interactions.csv", function(data) {

	// create a tooltip
	var tooltip = d3.select("#heatmap_chart")
		.append("div")
		//.append("g")
		.style("opacity", 0)
		.attr("class", "tooltip")
		.style("background-color", "white")
		.style("border", "solid")
		.style("border-width", "2px")
		.style("border-radius", "4px")
		.style("padding", "5px")
		.style("position", "absolute") //needed for div not g

	// Three function that change the tooltip when user hover / move / leave a cell
	var mouseover = function(d) {
		tooltip
			.style("opacity", 1)
		d3.select(this)
			.style("stroke", "black")
			.style("opacity", 1)
	}

	var mousemove = function(d) {
		//console.log(d3.mouse(this)[0])
		//console.log(d3.event.pageX)

		tooltip
			.html("" + d.value + " shared scenes")
			//.attr("x", 200)
			//.attr("y", 200)
			//.style("left", 200 + "px")
			//.style("top", 200 + "px")
			//.style("left", (d3.mouse(this)[0]) + "px")
			//.style("top", (d3.mouse(this)[1]) + "px")
			.style("left", (d3.event.pageX + 30) + "px")
			.style("top", (d3.event.pageY ) + "px")
			//.style("left", (d3.event.pageX + d3.select('svg').node().getBoundingClientRect().x + 70) + "px")
			//.style("top", (d3.event.pageY + d3.select('svg').node().getBoundingClientRect().y) + "px")
			//.attr("transform", "translate(" + (d3.mouse(this)[0]  + 20) + "," + (d3.mouse(this)[0] - 20) + ")");
	}



	var mouseleave = function(d) {
		tooltip
			.style("opacity", 0)
			.html("")
		d3.select(this)
			.style("stroke", "none")
			//.style("opacity", 0.8)
	}

	// add the squares
	svg.selectAll()
		.data(data, function(d) {return d.char_1+':'+d.char_2;})
		.enter()
		.append("rect")
			.attr("x", function(d) { return x(d.char_1) })
			.attr("y", function(d) { return y(d.char_2) })
			.attr("rx", 4)
			.attr("ry", 4)
			.attr("width", x.bandwidth() )
			.attr("height", y.bandwidth() )
		.style("fill", function(d) { return myColor(d.value)} )
		.on("mouseover", mouseover)
		.on("mousemove", mousemove)
		.on("mouseleave", mouseleave)
})


// Add title to graph
svg.append("text")
        .attr("x", 0)
        .attr("y", -30)
        .attr("text-anchor", "left")
        .style("font-size", "22px")
        .style("fill", "black")
        .text("Game of Thrones Interactions");

// Add subtitle to graph
svg.append("text")
        .attr("x", 0)
        .attr("y", -15)
        .attr("text-anchor", "left")
        .style("font-size", "14px")
        .style("fill", "grey")
        .style("max-width", 400)
        .text("Who shares screentime by total shared scenes");

