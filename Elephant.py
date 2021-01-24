from IPython.core.display import HTML
from string import Template

class Elephant:
    """
    Make animated elephants move around their space
    """
    def __init__(self, ipos=[100, 100], name=None, color='gray', size=30, speed=10):
        if not name: name = "anonymous"
        self.name = name
        self.stroke = color
        self.fill = color
        self.size = size
        self.ipos = ipos
        self.speed = 10
        self.actions = []

    def goto(self, position):
        self.actions.append(['goto', position])

    def forward(self, distance):
        self.actions.append(['forward', distance])

    def backward(self, distance):
        self.actions.append(['backward', distance])

    def left(self, angle):
        self.actions.append(['left', angle])

    def right(self, angle):
        self.actions.append(['right', angle])

    def change_speed(self, s):
        self.actions.append(['change_speed', s])

    def color(self, c):
        self.actions.append(['change_stroke', c])
    
    def fillcolor(self, c):
        self.actions.append(['change_fill', c])

    def change_size(self, s):
        self.actions.append(['size_change', s])

    def penup(self):
        self.actions.append(['penup'])

    def pendown(self):
        self.actions.append(['pendown'])

    def begin_fill(self):
        self.actions.append(['begin_fill'])

    def end_fill(self):
        self.actions.append(['end_fill'])

    def open_eyes(self):
        self.actions.append(['open_eyes'])

    def close_eyes(self):
        self.actions.append(['close_eyes'])


def show_me_my_elephants(habitat_size, *args):
    elephant_template = Template('''
        <svg id="the_svg"></svg>

        <script src="https://d3js.org/d3.v6.min.js"></script>
        <script>

        function move_em(elephant, new_pos) {
            let dist = Math.sqrt((new_pos[0]-elephant.g_holder.attr('x'))**2 + (new_pos[1]-elephant.g_holder.attr('y'))**2);
            let time_it_takes = dist / elephant.speed;

            if (elephant.drawing_lines) {
                // sneaky dasharray trick for animating a path from https://bl.ocks.org/basilesimon/f164aec5758d16d51d248e41af5428e4
                var totalLength = elephant.current_path.node().getTotalLength() + dist;
                elephant.current_path
                    .attr('d', elephant.current_path.attr('d') + ' L ' + String(new_pos[0]) + ' ' + String(new_pos[1]))
                    .attr("stroke-dasharray", totalLength + " " + totalLength)
                    .attr("stroke-dashoffset", totalLength - totalLength + dist)
                        .transition()
                            .duration(time_it_takes*100)
                            .attr("stroke-dashoffset", 0);

            }

            elephant.g_holder.transition()
                .duration(time_it_takes*100)
                .attr('transform', 'translate(' + String(new_pos[0]) + ', ' + String(new_pos[1]) + ')')
                .attr('x', new_pos[0])
                .attr('y', new_pos[1])
                .on("end", () => do_actions(elephant));

        }

        function fresh_line(elephant) {
            elephant.current_path = elephant.line_holder.append('path')
                .attr('stroke', elephant.stroke)
                .attr('fill', 'transparent')
                .attr('d', 'M ' + elephant.g_holder.attr('x') + ' ' + elephant.g_holder.attr('y'));
        }

        function do_actions(elephant) {
            if (elephant.actions.length == 0) {
                return 'done';
            } else {
                let action = elephant.actions.shift();
                let element = elephant.element;
                let current_rotate = Number(element.attr('rotation'));
                if (action[0].split('_')[0] == 'change') {
                    elephant[action[0].split('_')[1]] = action[1];
                    if (['change_fill', 'change_stroke'].indexOf(action[0])>-1) fresh_line(elephant);
                    do_actions(elephant);
                } else if (action[0]=='size_change') {
                    elephant.size = action[1];
                    element.transition()
                        .duration(1000)
                        .ease(d3.easeLinear)
                        .attr('x', -elephant.size/2)
                        .attr('y', -elephant.size*15/46)
                        .attr('width', elephant.size)
                        .on("end", () => do_actions(elephant));
                } else if (action[0] == 'goto') {
                    move_em(elephant, action[1]);
                } else if (['left', 'right'].indexOf(action[0])>-1) {
                    let rotate_amount = {'left': -1*action[1], 'right': action[1]}[action[0]];
                    let time_it_takes = Math.abs(rotate_amount)/elephant.speed
                    element.attr('rotation', current_rotate + rotate_amount)
                    element.transition()
                        .duration(time_it_takes*100)
                        .ease(d3.easeLinear)
                        .attr('transform', 'rotate('+String(current_rotate + rotate_amount)+', 0, 0)')
                        .on("end", () => do_actions(elephant));
                } else if (['forward', 'backward'].indexOf(action[0])>-1) {
                    let move_amount = {'backward': -1*action[1], 'forward': action[1]}[action[0]];
                    let new_x = Number(elephant.g_holder.attr('x')) + Math.cos((Math.PI*(current_rotate/180)))*move_amount;
                    let new_y = Number(elephant.g_holder.attr('y')) + Math.sin((Math.PI*(current_rotate/180)))*move_amount;
                    move_em(elephant, [new_x, new_y]);
                } else if (action[0] == 'penup') {
                    elephant.drawing_lines = false;
                    do_actions(elephant);
                } else if (action[0] == 'pendown') {
                    fresh_line(elephant);
                    elephant.drawing_lines = true;
                    do_actions(elephant);
                } else if (action[0] == 'end_fill') {
                    elephant.drawing_lines = false;
                    elephant.current_path.attr('fill', elephant.fill);
                    do_actions(elephant);
                } else if (action[0] == 'begin_fill') {
                    fresh_line(elephant);
                    elephant.drawing_lines = true;
                    do_actions(elephant);
                } else if (action[0] == 'open_eyes') {
                    element.transition() // not really a transition, just a pause
                        .duration(1000)
                        .ease(d3.easeLinear)
                        .attr('href', 'https://raw.githubusercontent.com/mjohnson11/Elephant/main/elephant_eyes_open.svg')
                        .on("end", () => do_actions(elephant));
                } else if (action[0] == 'close_eyes') {
                    element.transition() // not really a transition, just a pause
                        .duration(1000)
                        .ease(d3.easeLinear)
                        .attr('href', 'https://raw.githubusercontent.com/mjohnson11/Elephant/main/elephant.svg')
                        .on("end", () => do_actions(elephant));
                }
            }
        }

        var elephants = $elephants;
        var habitat_size = $habitat_size;
        var the_svg = d3.select('#the_svg')
        the_svg.attr('width', habitat_size[0]).attr('height', habitat_size[1]);
        console.log(elephants);

        for (let elephant of elephants) {

            elephant.drawing_lines = true;
            elephant.line_holder = the_svg.append('g'); // this is just to keep the layers right (lines behind)

            elephant.g_holder = the_svg.append('g')
                .attr('x', elephant.ipos[0])
                .attr('y', elephant.ipos[1])
                .attr('transform', 'translate(' + String(elephant.ipos[0]) + ', ' + String(elephant.ipos[1]) + ')');

            fresh_line(elephant);

            elephant.element = elephant.g_holder.append('image')
                .attr('href', 'https://raw.githubusercontent.com/mjohnson11/Elephant/main/elephant.svg')
                .attr('x', -elephant.size/2)
                .attr('y', -elephant.size*15/46)
                .attr('width', elephant.size)
                .attr('rotation', 0);

            do_actions(elephant)
        }

        </script>
        ''')
    display(HTML(elephant_template.substitute({'elephants': [a.__dict__ for a in args], 'habitat_size': habitat_size})))
