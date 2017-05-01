var width = 960,
    height = 1000;
    
var fill = d3.scale.category20();

var force = d3.layout.force()
    .charge(-500)
    .linkDistance(120)
    .size([width, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


d3.json("force.json", function(error, json) {
  if (error) throw error;

  var link = svg.selectAll("line")
      .data(json.links)
    .enter().append("line")
    .attr("class", "link");

  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g")
      .attr("class", "node")
      .style("fill", function(d) { return fill(d.group); })
      .style("stroke", function(d) { return d3.rgb(fill(d.group)).darker(); })
      .call(force.drag);
  
  node.append("circle")
      .style("fill", "#FF0000")
      .attr("r", 30);

  node.append("text")
      .attr("dx", ".25em")
      .attr("dy", ".35em")
      .attr("text-anchor", "middle")
      .style("stroke", function(d) { return fill(d.color); })
      .style("font-size", "14px")
      .text(function(d) { return d.name });

  force
      .nodes(json.nodes)
      .links(json.links)
      .on("tick", tick)
      .start();

  function tick(e) {
    var k = 5 * e.alpha;

    // Push sources up and targets down to form a weak tree.
    link
        .each(function(d) { d.source.y -= k, d.target.y += k; })
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

  }
});

/*width = 960,
height = 500,
fill = d3.scale.category20();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


var force = d3.layout.force()
    .gravity(0.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);

d3.json("force.json", function(error, json) {
  if (error) throw error;

  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link");

  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g")
      .attr("class", "node")
      .call(force.drag);

//append("image")
//      .attr("xlink:href", "https://github.com/favicon.ico")

  node.append("circle")
      .style("fill", "#FF0000")
      .attr("x", -8)
      .attr("y", -8)
      .attr("r", 45);

  node.append("text")
      .attr("dx", ".25em")
      .attr("dy", ".35em")
      .attr("text-anchor", "middle")
      .attr("stroke", function(d) { return fill(d.color); })
      .style("font-size", "14px")
      .text(function(d) { return d.name });

  force.on("tick", function() {

    var k = 3;

    link.each(function(d) { d.source.y -= k, d.target.y += k; })
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
});*/