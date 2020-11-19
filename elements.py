import sys


def get_valid_input(input_string, valid_options):
    input_string += f"({', '.join(valid_options)}) "
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        if "check" not in original_function.__name__:
            # print(f'wrapper executed wrapper_function before {original_function.__name__}')
            print("=============================================")
        return original_function(*args, **kwargs)

    return wrapper_function


class Component:
    def __init__(self, state="off"):
        self.state = state

    def is_working(self):
        return self.state


class Switch:

    map_values = {"off": 0, "intermittent": 1, "wipe": 2, "fast-wipe": 3}
    current_value = 0

    def __init__(self, state="off"):
        # self.map_values = {"off": 0, "intermittent": 1, "wipe": 2, "fast-wipe": 3, "wash": 4}
        self.state = state
        # print('alan')
        # self.__current_value = self.map_values[state]

    def get_state(self):
        # for keys in self.map_values.keys():
        #     if self.state == keys:
        #         # print(self.map_values[self.state])
        #         # self.__current_value = self.map_values[self.state]
        #         # print(self.__current_value)
        #         return self.map_values[self.state]
        #     # else:
        #     #     print('pashm', keys)
        # # x = list(self.map_values.keys())[list(self.map_values.values()).index(self.state)]
        # # print(x)
        return self.state

    # def move_up(self):
    #     Switch.current_value = Switch.map_values[self.state]
    #     print('in swi',Switch.current_value, Switch.map_values[self.state])
    #     print(type(Switch.current_value), Switch.current_value+1)
    #     # print('in fun',self.__current_value)
    #     if Switch.current_value < 4:
    #         print("move up".upper())
    #         Switch.current_value += 1
    #         print('final', Switch.current_value+1)
    #         # self.state =
    #     else:
    #         print(f"The switch cannot move up more.({self.state})")

    # @decorator_function
    # def move_down(self):
    #     Switch.current_value = Switch.map_values[self.state]
    #     if Switch.current_value > 0:
    #         print("move down".upper())
    #         Switch.current_value -= 1
    #     else:
    #         print(f"The switch cannot move down more.({self.state})")

    # # @decorator_function
    # def wash(self):
    #     print("wash".upper())


class WiperMotor(Component):
    def __init__(self, state="off", working="off"):
        super().__init__(state)
        self.working = working

    @decorator_function
    def display(self):
        print(f"The {__class__.__name__} mode is {self.working}.")

    def get_state(self):
        return self.working


class Pump(Component):
    def __init__(self, state="off", working="off"):
        super().__init__(state)
        self.working = working

    def display(self):
        print(f"The {__class__.__name__} mode is {self.working}.")

    def get_state(self):
        return self.working


class WatterBottle:
    def __init__(self, level=3):
        self.level = level

    def is_empty(self):
        return self.level <= 0

    def fill(self):
        self.level = 3
        return self.level

    def extract(self):
        self.level -= 1

    def get_level(self):
        return self.level


class SimulationClass:
    valid_modes = ("off", "intermittent", "wipe", "fast-wipe")

    def __init__(self):
        self.battery = Component()
        self.ecu = Component()
        self.switch = Switch()
        self.wiper = WiperMotor()
        self.pump = Pump()
        self.watter_bottle = WatterBottle()
        self.choices = {
            "1": self.start_wipe,
            "2": self.move_up,
            "3": self.move_down,
            "4": self.wash,
            "5": self.get_state,
            "0": self.finish,
        }

    @decorator_function
    def display(self):
        print(
            """Menu:
    1 : Start
    2 : move switch up
    3 : move switch down
    4 : wash
    5 : get switch mode
    0 : exit"""
        )

    @decorator_function
    def check(self, myfunc):
        # self.ecu.state = self.battery.is_working()
        if self.ecu.state != "off":
            # self.ecu.state = self.switch.get_state()
            # self.wiper.state = self.battery.is_working()
            # self.wiper.working = self.ecu.state
            myfunc()
        else:
            print(f"the Battery/ECU mode is {self.ecu.is_working()}.")

    def run(self):
        valid_prompt = ("1", "2", "3", "4", "5", "0")
        while True:
            self.display()
            user_input = get_valid_input("What option do you want? ", valid_prompt)
            action = self.choices[user_input]
            action()

    @decorator_function
    def start_wipe(self):
        self.switch.state = get_valid_input(
            "Which mode of wiper do you need?", SimulationClass.valid_modes
        )
        self.battery.state = get_valid_input("The battery state is?", ("on", "off"))
        while self.battery.is_working() != "on":
            print(
                """=======================\nThe battery must be on.\n======================="""
            )
            if get_valid_input("Do you want to continue?", ("yes", "no")) == "yes":
                self.run()
            else:
                self.finish()

        # if the battery is on, so the ECU and wiper are on.
        self.ecu.state = self.battery.is_working()
        self.wiper.state = self.ecu.state

        # the the ECU gets the switch state.
        self.ecu.state = self.switch.get_state()

        Switch.current_value = Switch.map_values[self.ecu.is_working()]
        self.wiper.working = self.ecu.is_working()

        self.wiper.display()

    @decorator_function
    def move_up(self):
        self.ecu.state = self.battery.is_working()
        if self.ecu.state != "off":
            self.wiper.state = self.ecu.is_working()
            self.ecu.state = self.switch.get_state()
            if Switch.current_value < 3:
                Switch.current_value += 1
                self.ecu.state = list(Switch.map_values.keys())[
                    list(Switch.map_values.values()).index(Switch.current_value)
                ]
                self.wiper.working = self.ecu.is_working()
                self.wiper.display()
            else:
                print(
                    f"The switch cannot move up more.(switch current mode: fast-wipe)"
                )

        else:
            print(
                """=======================\nThe battery must be on.\n======================="""
            )
            if get_valid_input("Do you want to continue?", ("yes", "no")) == "yes":
                self.run()
            else:
                self.finish()

    @decorator_function
    def move_down(self):
        #     self.check(self.switch.move_down)
        self.ecu.state = self.battery.is_working()
        if self.ecu.state != "off":
            self.wiper.state = self.ecu.is_working()
            self.ecu.state = self.switch.get_state()
            if Switch.current_value > 0:
                Switch.current_value -= 1
                self.ecu.state = list(Switch.map_values.keys())[
                    list(Switch.map_values.values()).index(Switch.current_value)
                ]
                self.wiper.working = self.ecu.is_working()
                self.wiper.display()
            else:
                print(f"The switch cannot move down more.(switch current mode: off)")

        else:
            print(
                """=======================\nThe battery must be on.\n======================="""
            )
            if get_valid_input("Do you want to continue?", ("yes", "no")) == "yes":
                self.run()
            else:
                self.finish()

    @decorator_function
    def get_state(self):
        print(f"The switch mode is {self.switch.get_state()}.".upper())

    @decorator_function
    def wash(self):
        # self.check(self.switch.wash)

        self.ecu.state = self.battery.is_working()
        self.switch.state = "wash"
        if self.ecu.state != "off":
            self.pump.state = self.ecu.is_working()
            self.ecu.state = self.switch.get_state()
            self.pump.working = self.ecu.is_working()
            if not self.watter_bottle.is_empty():
                self.watter_bottle.extract()
                self.pump.display()
            else:
                print(
                    """=======================\nThe water bottle is empty.\n======================="""
                )
                if get_valid_input("Do you want to fill?", ("yes", "no")) == "yes":
                    self.watter_bottle.fill()
                else:
                    self.run()

        else:

            print(
                """=======================\nThe battery must be on.\n======================="""
            )
            if get_valid_input("Do you want to continue?", ("yes", "no")) == "yes":
                self.battery.state = get_valid_input(
                    "Which battery state? ", ("on", "off")
                )
                self.run()
            else:
                self.finish()

    @decorator_function
    def finish(self):
        print("EXIT")
        sys.exit(-1)


if __name__ == "__main__":
    SimulationClass().run()
