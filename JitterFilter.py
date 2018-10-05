import math
import numpy
print("Program Start")

test = 3
lower_cartesian_threshold = 0.0 # Below this level no movement occurs
high_cartesian_threshold = 0.0 # Above this level no movement occurs
cartesian_movement_scaling = 0.0 # How far the coordinates should move from represented to estimated (values 0 - 1)

lower_angle_threshold = 0.0 # Below this level no movement occurs
high_angle_threshold = 0.0 # Above this level no movement occurs
orientation_scaling = 0.0 # How far the orientation moves from represented to estimated(values 0 - 1)

distance_scaling_range = 0.0 # range over which the distance scaling is changed
orientation_scaling_range = 0.0 # range over which the angle scaling is changed
# Represented Cartesian Coordinates
x_represented = 0.0
y_represented = 0.0
z_represented = 0.0
# Represented Unit Vectors
x_axis_represented = numpy.array([[0.0],[0.0],[0.0]])
y_axis_represented = numpy.array([[0.0],[0.0],[0.0]])
z_axis_represented = numpy.array([[0.0],[0.0],[0.0]])
print(x_axis_represented)

# Estimated Cartesian Coordinates
x_estimated = 0.0
y_estimated = 0.0
z_estimated = 0.0

# Estimated Unit Vectors
x_axis_estimated = numpy.array([4.0,4.0,4.0])
y_axis_estimated = numpy.array([9.0,9.0,9.0])
z_axis_estimated = numpy.array([3.0,3.0,3.0])

def starting_function():
    global x_represented, y_represented, z_represented, x_estimated, y_estimated, z_estimated
    global x_axis_represented, y_axis_represented, z_axis_represented, x_axis_estimated, y_axis_estimated, z_axis_estimated
    x_represented = x_estimated
    y_represented = y_estimated
    z_represented = z_estimated
    x_axis_represented = x_axis_estimated
    y_axis_represented = y_axis_estimated
    z_axis_represented = z_axis_estimated
    print("start")
    return



def calculate_new_represented_position():
    global x_estimated, y_estimated, z_estimated, x_represented, y_represented, z_represented
    global lower_cartesian_threshold, high_cartesian_threshold, distance_scaling_range
    # find euclidean distance between represented position and estimated position
    difference_x = x_estimated - x_represented
    difference_y = y_estimated - y_represented
    difference_z = z_estimated - z_represented
    distance = math.sqrt((difference_x)**2 + (difference_y)**2 + (difference_z)**2)
    # only move the represented position if a lower threshold is breached, and the high threshold is not breached
    if distance > lower_cartesian_threshold and distance < high_cartesian_threshold:
        if distance >= distance_scaling_range:
            cartesian_movement_scaling = 1
        elif distance < distance_scaling_range:
            cartesian_movement_scaling = distance/distance_scaling_range
        x_represented = x_represented + cartesian_movement_scaling*(difference_x)
        y_represented = y_represented + cartesian_movement_scaling*(difference_y)
        z_represented = z_represented + cartesian_movement_scaling*(difference_z)


    return

def calculate_new_represented_orientation():
    global x_axis_estimated, y_axis_estimated, z_axis_estimated, x_axis_represented, y_axis_represented, z_axis_represnted, test
    global lower_angle_threshold, high_angle_threshold, orientation_scaling_range
    print(x_axis_represented)
    print(test)
    # Calculate Angle between 2 represntation and orientation vectors
    combined_estimation_vector = x_axis_estimated + y_axis_estimated + z_axis_estimated
    print(x_axis_estimated)
    print(combined_estimation_vector)
    combined_representation_vector = x_axis_represented + y_axis_represented + z_axis_represented
    print(combined_representation_vector)
    angle_between_vectors =  math.acos(combined_estimation_vector.dot(combined_representation_vector))  # Be aware, having unit vectors has simplified this, also not using unit vectors most likely makes an error, as acos not defined for everything
    print(angle_between_vectors)
    
    # only move the represented orientation if a lower threshold is breached, and the high threshold is not breached
    #if angle_between_vectors > lower_angle_threshold and angle_between_vectors < high_angle_threshold:
    #    if angle_between_vectors >= orientation_scaling_range:
    #        orientation_scaling_scaling = 1
    #    elif angle_between_vectors < orientation_scaling_range:
    #        orientation_scaling = angle_between_vectors/orientation_scaling_range
    #
    #    x_axis_represented = (x_axis_estimated - x_axis_represented)*orientation_scaling_range
    #    x_axis_represented = x_axis_represented/(numpy.sqrt(x_axis_represented.dot(x_axis_represented))) #normalise to unit vector so it is good next time round
    #    y_axis_represented = (y_axis_estimated - y_axis_represented)*orientation_scaling_range
    #    y_axis_represented = y_axis_represented/(numpy.sqrt(y_axis_represented.dot(y_axis_represented))) #normalise to unit vector so it is good next time round
    #    z_axis_represented = (z_axis_estimated - z_axis_represented)*orientation_scaling_range
    #    z_axis_represented = z_axis_represented/(numpy.sqrt(z_axis_represented.dot(z_axis_represented))) #normalise to unit vector so it is good next time round
    return
starting_function()
calculate_new_represented_position()
calculate_new_represented_orientation()




