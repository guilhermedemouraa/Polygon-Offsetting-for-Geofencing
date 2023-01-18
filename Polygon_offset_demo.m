clear; clc

polygon{1} = [1,1;0,1.5;-1,1;-1,-1;0,-1.5;1,-1]; % --> Hexagon centered at (0,0)
polygon{2} = [0,0;2,0;2,2;0,2]; %% --> Simple square
polygon{3} = [1.9,1;4,1.6;3.63,2.52;5,3.5;2.66,4.71;0.72,2.28;1,1.5]-3; % --> Irregular polygon
polygon{1} = [1,-1;0,-1.5;-1,-1;-1,1;0,1.5;1,1]; %--> illustrates what
%would happen if polygon data points were given in clockwise order
s = 0;
for i = 1:3
    for j = 1:2
        s = s+1;
        if j == 1
            direction = 'o'; % --> outward offset
        else
            direction = 'i';
        end
        pol = polygon{i};
        offset = 1;
        [buff_pol] = polygon_offset(pol, offset, direction);
        pol = [pol;pol(1,1),pol(1,2)];
        buff_pol = [buff_pol; buff_pol(1,1),buff_pol(1,2)];
        x = pol(:,1); y = pol(:,2); x_buffer = buff_pol(:,1); y_buffer = buff_pol(:,2);
        subplot(3,2,s)
        plot(x,y,'r--o');
        xlim([-10,10]);ylim([-10,10]);
        hold on;
        plot(x_buffer,y_buffer,'b-o');
        legend('Original polygon', 'Buffered polygon');
    end
end