import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import socket


# Host and port for socket connection with unity
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024

# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3D model points of the QR-Code(If QR-Code dimentions change, change this)
model_points = np.array([
    (-21.5, 21.5, 0.0),
    (-21.5, -21.5, 0.0),
    (21.5, -21.5, 0),
    (21.5, 21.5, 0.0)
])

# Get video from file or camera device, if only a single camera connected use default ID 0
# otherwise determine ID of the desired camera.
cap = cv2.VideoCapture(0)

# Load image from camera feed into frame
ret, frame = cap.read()

# Check if frame is successfully captured
if not ret:
    print('Image could not be captured')

# Camera internals
size = frame.shape
focal_length = size[1]
print(size[1])
print(size[0])
center = (size[1] / 2, size[0] / 2)
camera_matrix = np.array(
    [[focal_length, 0, center[0]],
     [0, focal_length, center[1]],
     [0, 0, 1]], dtype="double"
)
dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Otsu's thresholding after Gaussian filtering
    #blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Decode QR-Code in the frame
    decodedObjects = pyzbar.decode(frame)

    # Gather results
    points = []
    data = ''
    for obj in decodedObjects:
        # points = obj.polygon
        data = obj.data
        points = obj.type

    if points:

        # 2D image points of the QR-Code
        image_points = np.array([
            (points[0][0], points[0][1]),
            (points[1][0], points[1][1]),
            (points[2][0], points[2][1]),
            (points[3][0], points[3][1])
        ], dtype="double")

        # Determine rotation and translation of QR-Code in the image
        success, rvec, tvec = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)

        # Decode and split data from QR-Code
        dvec = data.decode("utf-8").split(",")

        # Check if able to determine the rotation and translation of the QR-Code
        if success:
            # Convert to rotation matrix since rvec is a compact angle notation method
            rvec_matrix = cv2.Rodrigues(rvec)[0]

            # Create projection(transformation) matrix containing rotation matrix and transltation
            proj_matrix = np.hstack((rvec_matrix, tvec))

            # Decompose projection matrix into euler angles
            euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)[6]

            # Create package to be send via UDP stream
            # Package containing (X,Y,Z,R,P,Y)
            package = [tvec.item(0), tvec.item(1), tvec.item(2), euler_angles.item(0),
                       euler_angles.item(1), euler_angles.item(2)]

            # Round floating point numbers to 2 decimals for faster communication
            # and since float is too long for singles in Unity
            float_package_short = [round(x, 2) for x in package]

            # Convert to a string with a "," delimiter
            s_package = ','.join(str(e) for e in float_package_short)

            # Lastly the secound QR-code data item is put in the package since it is a string
            # and since it is sometimes miss read(leading to program exit if (try-except) is not used.
            s_package += ','
            try:
                s_package += dvec[1]
            except IndexError:
                s_package += '7'

            # Converting string package to bit package for transmission
            b_package = bytes(s_package, 'utf-8')

            # Sending package via UDP stream
            s.sendto(b_package, (UDP_IP, UDP_PORT))

    # Display the resulting frame
    #cv2.imshow('frame', frame)
    #cv2.imshow('th3', th3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()