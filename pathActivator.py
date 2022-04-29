from distutils.log import debug
from sender import Sender
import re


# The COM port should be changed to the correct one found on the machine
# can leave empty if using linux?
#s.send('+2')



class PathActivator:
    VALID_REGEX = "[AC][0-9]{2}|SUB"
    MAX_A_VALUE = 15
    SUB_TOP = ["C_SUB_Odd_SEL1", "Odd_Even_SEL1", "C_A_CTRL1"]
    SUB_BOT = ["C_SUB_Odd_SEL2", "Odd_Even_SEL2", "C_A_CTRL2"]
    C_TOP = "C_A_CTRL1"
    C_BOT = "C_A_CTRL2"
    ODD_TOP = "Odd_Even_SEL1"
    ODD_BOT = "Odd_Even_SEL2"
    POS_TO_PAIR = {
        "A00" : "A0_A1",
        "A01" : "A0_A1",
        "A02" : "A2_A3",
        "A03" : "A2_A3",
        "A04" : "A4_A5",
        "A05" : "A4_A5",
        "A06" : "A6_A7",
        "A07" : "A6_A7",
        "A08" : "A8_A9",
        "A09" : "A8_A9",
        "A10" : "A10_A11",
        "A11" : "A10_A11",
        "A12" : "A12_A13",
        "A13" : "A12_A13",
        "A14" : "A14_A15",
        "A15" : "A14_A15",

        "C00" : "C0_C1",
        "C01" : "C0_C1",
        "C02" : "C2_C3",
        "C03" : "C2_C3",
        "C04" : "C4_C5",
        "C05" : "C4_C5",
        "C06" : "C6_C7",
        "C07" : "C6_C7",
        "C08" : "C8_C9",
        "C09" : "C8_C9",
        "C10" : "C10_C11",
        "C11" : "C10_C11",
        "C12" : "C12_C13",
        "C13" : "C12_C13",
        "C14" : "C14_C15",
        "C15" : "C14_C15",
    }


    def __init__(self, COM_port, debug = False):
        self.sender = Sender(COM_port)
        self.debug = debug

    # Activates all the right choices to get to the selected output
    def activate_path_to(self, red_output, black_output):
        path = self.__get_path_to(red_output, black_output)
        # turns off all the pins
        self.sender.send("reset()")
        message = self.sender.receive()
        if (self.debug):
            print (message)

        for pin in path:
            # turns on only the pins in the path
            self.sender.send("turn_on(\""+pin+"\")")
            message = self.sender.receive()
            if (self.debug):
                print (message)
        


    # Calculates all the right choices to get to the selected output
    def __get_path_to(self, red_output, black_output):
        if self.__isValid__ (red_output, black_output) != True:
            return []
        else:
            # Here will be stored all the pins that need to be activated
            path = []
            # This handles the red output
            if (red_output == "SUB"):
                path.extend(PathActivator.SUB_TOP)
            else:
                red_letter = red_output[0]
                red_number = int(red_output[1:])
                # Picks the first relay to be the pair
                path.append(PathActivator.POS_TO_PAIR[red_output])
                # The 2nd relay is 0 since we don't want to get SUB anyways
                # The 3rd relay is based on the parity of the output
                if red_number % 2:
                    path.append(PathActivator.ODD_TOP)
                # The 4th relay is based on whether the output is A or C
                if red_letter == 'C':
                    path.append(PathActivator.C_TOP)

            # This handles the black output
            if (black_output == "SUB"):
                path.extend(PathActivator.SUB_BOT)
            else:
                black_letter = black_output[0]
                black_number = int(black_output[1:])
                # Picks the first relay to be the pair
                path.append(PathActivator.POS_TO_PAIR[black_output])
                # The 2nd relay is 0 since we don't want to get SUB anyways
                # The 3rd relay is based on the parity of the output
                if black_number % 2:
                    path.append(PathActivator.ODD_BOT)
                # The 4th relay is based on whether the output is A or C
                if black_letter == 'C':
                    path.append(PathActivator.C_BOT)
            # return and remove dups
            return list(dict.fromkeys(path))

    def __isValid__(self, red_output, black_output):
        # Length check
        if len(red_output)!= 3 or len(black_output)!= 3:
            print("Wrong length of output, try: \"SUB or \"A01 for example")
            return False
        # Regex check
        is_valid_regex = True
        red_pos = re.search(PathActivator.VALID_REGEX, red_output)
        black_pos = re.search(PathActivator.VALID_REGEX, black_output)
        if red_pos == None:
            is_valid_regex= False
            print(red_output + " is an invalid output")
        if black_pos == None:
            is_valid_regex= False
            print(black_output + " is an invalid output")
        if (is_valid_regex == False):
            return False
        # Too big output number check
        if red_output[0] != 'S' and int(red_output[1:]) > PathActivator.MAX_A_VALUE:
            print("Try smaller numbers for red_output")
            return False
        if black_output[0] != 'S' and int(black_output[1:]) > PathActivator.MAX_A_VALUE:
            print("Try smaller numbers for black_output")
            return False
        # Impossible output combination check
        
        if red_output[0] == black_output[0] and red_output[0] != 'S':
            if (int(int(red_output[1:])/2) != int(int(black_output[1:])/2)):
                print("Impossible output combination")
                return False
        return True




    def close(self):
        self.sender.close()