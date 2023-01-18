function [newpolygon] = polygon_offset(polygon, offset, direction)
% polygon_offsets takes a set of 2D coordinates that make a polygon, an
% offseting distance, and a desired direction to calculate new
% coordinates that make an offset polygon.

% INPUTS:
% polygon: 2D array containing the coordinates of all vertices of a polygon
% offset: desired offset distance
% direction: direction at which the offset is desired 'i' for inward or
% 'o' for outward

% OUTPUT: 2D array containing the coordinates of all vertices
% of the buffered polygon

% EXAMPLE:
%{
polygon = [1,1;0,1.5;-1,1;-1,-1;0,-1.5;1,-1]; % --> Hexagon centered at (0,0)
offset = 1;
direction = 'o'; % --> outward offset
buff_pol = polygon_offset(polygon, offset, direction);
% >> RESULT: buff_pol = [1.85065080835204,1.52573111211913;0,2.50; -1.85065080835204,1.52573111211913;
% -1.85065080835204,-1.52573111211913;0,-2.50;1.85065080835204,-1.52573111211913]
polygon = [polygon;polygon(1,1),polygon(1,2)];
buff_pol = [buff_pol; buff_pol(1,1),buff_pol(1,2)];
x = polygon(:,1); y = polygon(:,2); x_buffer = buff_pol(:,1); y_buffer = buff_pol(:,2);
plot(x,y,'r--o');
xlim([-10,10]);ylim([-10,10]);
hold on;
plot(x_buffer,y_buffer,'b-o');
legend('Original polygon', 'Buffered polygon');
%}
%% Part 1: Define directional vectors for each side of the polygon and find normal(perpendicular) vectors for each of directional vectors

polygon = [polygon;polygon(1,1),polygon(1,2)]; % Copy first vertice of polygon to "close it"

x = polygon(:,1); y = polygon(:,2);
dx = zeros(length(polygon)-1,1); dy = dx; n = zeros(length(dx),2); ns{1,length(dx)} = [];

for i = 1:length(polygon)-1
    dx(i) = polygon(i+1,1)-polygon(i,1);
    dy(i) = polygon(i+1,2)-polygon(i,2);
    if dy(i) == 0
        dy(i) = 1e-16; % Forces algorithm to convert if there's a horizontal line
    end
    n(i,1) = 1; n(i,2) = -dx(i)/dy(i); % Create a normal vector to the current side of the polygon
    norm(i) = sqrt(n(i,1)^2+n(i,2)^2);
    n(i,:) = n(i,:)/norm(i); % Normalizes perpendicular vector (||vector|| = 1)
    ns{i} = n(i,:); % Cell containing all normal vectors
end

% Evaluates a series of conditions to ensure that the perpendicular vectors
% all point to the same direction (i.e., all inwards or all outwards)

for i = 1:length(ns)
    if dx(i) < 0 && dy(i) < 0
        ns{i} = -1* ns{i};
    elseif dx(i) == 0 && dy(i) < 0
        ns{i} = -1* ns{i};
    elseif dx(i) > 0 && dy(i) < 0
        ns{i} = -1* ns{i};
    end
end
%% Part 2: Define bisectors for each pair of normal vectors
% Source: https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges

bis{1,length(ns)} = [];
bis{1} = (ns{length(n)}+ns{1})./sqrt(2);

for i = 2:length(n)
    bis{i} = (ns{i-1}+ns{i})./sqrt(2);
end

l = zeros(length(bis),1);
l(1) = offset./sqrt(1+sum(ns{length(n)}.*ns{1}));

for i = 2:length(n)
    l(i) = offset./sqrt(1+sum(ns{i-1}.*ns{i}));
end

newpolygon = [];
for i = 1:length(polygon)-1
    newpolygon = [newpolygon; [x(i) y(i)] + l(i) * bis{i}];
end

%% Part 3: Checks orientation of dataset (clockwise vs. counter clockwise)
% Calculate ratio of areas for original and new polygons.
% If original area > new area --> Polygon was offset inwards
% If original area < new area --> Polygon was offset outwards
% Polygon offseting direction is checked against desired offsetting
% direction and corrected accordingly.

x_o = newpolygon(:,1); y_o = newpolygon(:,2); x_o = [x_o;x_o(1)]; y_o = [y_o;y_o(1)]; 

j = length(dx); area = 0.0; area_b = 0;
for i = 1:length(dx)
    area = area + (x(j) + x(i)) * (y(j) - y(i));
    area_b = area_b + (x_o(j) + x_o(i)) * (y_o(j) - y_o(i));
    j = i;
end

area = abs(area)/2.0; area_b = abs(area_b)/2.0;

if area > area_b && direction == 'o' || area < area_b && direction == 'i'
    for i = 1:length(ns) % Adjusts vectors direction in case of inward offsetting
        ns{i} = -ns{i};
    end
    bis{1,length(ns)} = [];
    bis{1} = (ns{length(n)}+ns{1})./sqrt(2);

    for i = 2:length(n)
        bis{i} = (ns{i-1}+ns{i})./sqrt(2);
    end

    l = zeros(length(bis),1);
    l(1) = offset./sqrt(1+sum(ns{length(n)}.*ns{1}));

    for i = 2:length(n)
        l(i) = offset./sqrt(1+sum(ns{i-1}.*ns{i}));
    end

    newpolygon = [];
    for i = 1:length(polygon)-1
        newpolygon = [newpolygon; [x(i) y(i)] + l(i) * bis{i}];
    end
    x_o = newpolygon(:,1); y_o = newpolygon(:,2);
end