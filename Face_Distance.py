import cv2 as cv
import dlib as dl 

#method which finds the Focal length which is used to calculate the distances
def Focal_Length_Finder(Measured_distance, Measured_Height, Pixel_P_Height):
    # Distance from camera to object(Measured_Height) Multiplied with object height in the image(Pixel_P_Height)
    # whole divided by Measured_Height( object height in the real world)
    Focal_length = (Pixel_P_Height* Measured_distance)/Measured_Height
    return Focal_length

#Method which calculates the distance from the object to camera
def Distance_Finder(Measured_Height, Focal_Length, Pixel_Per_Height):
    # Real_world_Height(Measured_Height) multiplied with Focal_Length(Focal_Length), 
    # whole divide by the Object height in the Image(Pixel_Per_Height)
    Distance = (Measured_Height * Focal_Length)/Pixel_Per_Height    
    return Distance

Measured_Height = 6 #inches

Measured_Distance = 24 #inches

# intilization dlib face detector 
Face_Detector = dl.get_frontal_face_detector()

# Reading reference image for Directory 


img =cv.imread("images/image.jpg")

gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

Faces = Face_Detector(gray)
print(img.shape)
for Face in Faces:
    #getting points of rectangle around the face
    right, top = Face.right(), Face.top()
    left, bottom = Face.left(), Face.bottom()
    
    # finding the height and width of image 
    height,width =gray.shape
    
    # drawing Rectangle arrouding the face
    cv.rectangle(img, (left, top),(right, bottom), (0,0,255),2)
    # print(left, top, right, bottom )
    
   
    # finding the height of face by subtracting top from the bottom points of rectangles 
    face_height= -top +bottom
    # print(face_width, face_height)
    focal_lenght=Focal_Length_Finder(Measured_Distance, Measured_Height, face_height)
    found_distance =Distance_Finder(Measured_Height, focal_lenght, face_height)
# cv.imshow("window", img)

#Intilization of camera object

cap = cv.VideoCapture(0)

#runing main loop every incoming frame read in while loop(from camera or video)
while True:
    # getting frame for the camera
        
    _, frame = cap.read()
    
    # finding the width, height dim , of frame 
    width, height, dim = frame.shape
    
    # print(f"width = {width} _ Height = {height}")
    
    gray =cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    # Detecting Faces
    Faces = Face_Detector(gray)
    # Looping through faces
    for Face in Faces:
        # Getting Detected face points
        Right, Left = Face.right(), Face.left()
        Top, Bottom = Face.top(), Face.bottom()
        # drawing Rectangle
        cv.rectangle(frame, (Left, Top), (Right, Bottom), (0, 223, 255), 1)
        # Getting height of face by subtracting Top from Bottom of face
        Face_Hight_pph = Bottom - Top
        # Getting distance using distance method 
        distance = Distance_Finder(Measured_Height, focal_lenght, Face_Hight_pph )
        text= f"Distance= {round(distance,2)} Inches"
        # putting distance on Screen 
        cv.putText(frame, text, (50,50), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    # showing the frame on the screen through window
    cv.imshow("Window", frame )
    #breaking/ going out of loop when specified Key is press on keyboard/ by using waitKey function opencv 
    if cv.waitKey(1)==ord("q"):
        # if q key pressed on the keyboard break the loop
        break
    
#closing All windows,
cv.destroyAllWindows()
# closing the camera, 
cap.release()
