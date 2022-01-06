def grid_rectangle(draw, width, height, interval, gap, grid) :
    '''
    interval * (n) + gap * (n-1) < width < interval * (n+1) + gap * (n)
    side = width - (interval * n + gap * (n-1))
    '''
    if grid == 0 :
        colour = 'white'
    else :
        colour = 'grey'

    n_width = int(math.floor((width + gap) / (interval + gap)))
    n_height = int(math.floor((height + gap) / (interval + gap)))

    side_width = 0.5 * (width - (interval * n_width + gap * (n_width-1)))
    side_height = 0.5 * (height - (interval * n_height + gap * (n_height-1)))

    box_number = n_width * n_height
    box_info = np.zeros((box_number, 4))

    start_vertex = [side_width, side_height]
    print(f'n_width = {n_width}, n_height = {n_height}')
    
    for index in range(box_number) :
        now_x = int(index % n_width)
        now_y = int(index // n_width)
        
        # box_info 0, 1 are (x, y) for the left-top vertex
        box_info[index, 0] = start_vertex[0] + interval * now_x + gap * now_x
        box_info[index, 1] = start_vertex[1] + interval * now_y + gap * now_y
        
        # box info 2, 3 are (x, y) for the right-bottom vertex
        box_info[index, 2] = start_vertex[0] + interval * (now_x + 1) + gap * (now_x + 1)
        box_info[index, 3] = start_vertex[1] + interval * (now_y + 1) + gap * (now_y + 1)

    for index in range(box_number) :
        now_draw_list = box_info[index, :].tolist()
        draw.rectangle(now_draw_list, fill = None, outline = colour, width = 1)

    return box_info, side_width, side_height


def h_of_box(x_smpl, box_info) :
    x_smpl = x_smpl.transpose()
    hsv_value = []
    for index in range(box_info.shape[0]) :

        left_x = int(box_info[index, 0])
        right_x = int(box_info[index, 2])
        left_y = int(box_info[index, 1])
        right_y = int(box_info[index, 3])

        tmp_array = x_smpl[left_x : right_x, left_y : right_y]

#        image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
#        draw2 = ImageDraw.Draw(image)
#        draw2.rectangle((left_x, left_y, right_x, right_y), fill = 'black', outline = 'black', width = 1)
#        dlt.savepng(image, plot_dir, f'canvas_{index}.png')

        hsv_value.append((tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))


    return hsv_value


def s_of_box(x_smpl, box_info) :
    x_smpl = x_smpl.transpose()
    hsv_value = []
    for index in range(box_info.shape[0]) :

        left_x = int(box_info[index, 0])
        right_x = int(box_info[index, 2])
        left_y = int(box_info[index, 1])
        right_y = int(box_info[index, 3])

        tmp_array = x_smpl[left_x : right_x, left_y : right_y]

#        image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
#        draw2 = ImageDraw.Draw(image)
#        draw2.rectangle((left_x, left_y, right_x, right_y), fill = 'black', outline = 'black', width = 1)
#        dlt.savepng(image, plot_dir, f'canvas_{index}.png')

        hsv_value.append((tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))


    return hsv_value


def v_of_box(x_smpl, box_info) :
    x_smpl = x_smpl.transpose()
    hsv_value = []
    for index in range(box_info.shape[0]) :

        left_x = int(box_info[index, 0])
        right_x = int(box_info[index, 2])
        left_y = int(box_info[index, 1])
        right_y = int(box_info[index, 3])

        tmp_array = x_smpl[left_x : right_x, left_y : right_y]

#        image = Image.new(mode = 'P', size = (smpl_width, smpl_height), color = 'white')
#        draw2 = ImageDraw.Draw(image)
#        draw2.rectangle((left_x, left_y, right_x, right_y), fill = 'black', outline = 'black', width = 1)
#        dlt.savepng(image, plot_dir, f'canvas_{index}.png')

        hsv_value.append(255 - (tmp_array.sum().sum() / (tmp_array.shape[0] * tmp_array.shape[1])))


    return hsv_value



def internal_division(a, b, m, n) :
    return (a * n + b * m) / (m + n)



def hsv_to_circle(draw, interval, hsv_value, box_info) :
    min_radius = 0 #interval / 4
    max_radius = interval / 2
    
    radius_value = []

    # change hsv to radius
    hsv_rev = [x for x in hsv_value if x != 0]

    min_hsv = min(hsv_rev)
    max_hsv = max(hsv_rev)
    ave_hsv = sum(hsv_rev) / len(hsv_rev)

    # floor some values
    for i in range(len(hsv_value)) :
        if float(hsv_value[i]) <= 0.5 * ave_hsv :
            hsv_value[i] = 0


    for hsv in hsv_value :
        if hsv == 0 :
            radius_value.append(0)
        else :
            ratio = (hsv - min_hsv) / (max_hsv - min_hsv)
            if ratio < 0 :
                radius_value.append(0)
            else :
                radius_value.append(internal_division(min_radius, max_radius, ratio, 1 - ratio))


    for index in range(box_info.shape[0]) :
        left_x = box_info[index, 0]
        right_x = box_info[index, 2]
        left_y = box_info[index, 1]
        right_y = box_info[index, 3]

        midpoint = [0.5 * (left_x + right_x), 0.5 * (left_y + right_y)]
        radius = radius_value[index]
        
        ellipse_points = [midpoint[0] - radius, midpoint[1] - radius, \
                          midpoint[0] + radius, midpoint[1] + radius]
        if radius != 0 :
            draw.ellipse(ellipse_points, fill = 'black', outline = 'black')
        
