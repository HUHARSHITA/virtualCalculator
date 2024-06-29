import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, frame):
        cv2.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0,255, 255), cv2.FILLED)  #blue green red
        cv2.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 0, 0), 3)
        cv2.putText(frame, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y, frame):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 255, 255), cv2.FILLED)
            cv2.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 0,0), 3)
            cv2.putText(frame, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 5)
            return True
        return False

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # width
    cap.set(4, 720)   # height
    #address="https://192.168.225.210:8080/video"
    #cap.open(address)
    

    detector = HandDetector(detectionCon=0.5, maxHands=1)

    # Creating Buttons
    buttonListValues = [["7", "8", "9", "+"],
                        ["4", "5", "6", "-"],
                        ["1", "2", "3", "*"],
                        [".", "0", "=", "/"],
                        ["C"]]
    buttonList = []
    for y in range(5):
        for x in range(4):
            xpos = x * 100 + 800
            ypos = y * 100 + 150
            if y == 4 and x > 0:
                break
            buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

    # Variables
    myEquation = ''
    delayCounter = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            hands, frame = detector.findHands(frame, flipType=False)

            # Draw all buttons
            cv2.rectangle(frame, (800, 70), (800 + 400, 70 + 100), (0, 255, 255), cv2.FILLED)
            cv2.rectangle(frame, (800, 70), (800 + 400, 70 + 100), (255, 0,0), 3)
            for button in buttonList:
                button.draw(frame)

            # Check for Hand
            if hands:
                lmList = hands[0]["lmList"]
                if lmList:
                    point1 = lmList[8][:2]
                    point2 = lmList[12][:2]
                    length, info, frame = detector.findDistance(point1, point2, frame)
                    # print(length)
                    x, y = lmList[8][:2]
                    if length < 50:
                        for i, button in enumerate(buttonList):
                            if button.checkClick(x, y, frame) and delayCounter == 0:
                                myValue = button.value
                                if myValue == "C":
                                    myEquation = ""
                                elif myValue != "=":
                                    myEquation += myValue
                                else:
                                    try:
                                        myEquation = str(eval(myEquation))
                                    except ZeroDivisionError:
                                        myEquation = "Error"
                                    except Exception:
                                        myEquation = "Error"
                                delayCounter = 1

            if delayCounter != 0:
                delayCounter += 1
                if delayCounter > 10:
                    delayCounter = 0

            # Display equation
            cv2.putText(frame, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
