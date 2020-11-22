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
    map_values = ["off", "intermittent", "wipe", "fast-wipe"]
    current_value = 0

    def __init__(self, state="off"):
        self.state = state

    def get_state(self):
        return self.state

    def move_up(self):
        try:
            Switch.current_value += 1
            self.state = Switch.map_values[Switch.current_value]
        except IndexError:
            print("The switch cannot move up more.(switch current mode: fast-wipe)")
            return Switch.map_values[-1]
        else:
            return Switch.map_values[Switch.current_value]

    def move_down(self):
        try:
            if Switch.current_value > 0:
                Switch.current_value -= 1
                self.state = Switch.map_values[Switch.current_value]
            else:
                raise ValueError
        except ValueError:
            print("The switch cannot move down more.(switch current mode: off)")
            return Switch.map_values[0]
        else:
            return Switch.map_values[Switch.current_value]


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
        print(f"The {__class__.__name__} mode is wash.")

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
    valid_modes = ("off", "intermittent", "wipe", "fast-wipe", "wash")

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
        self.wiper.working = self.ecu.is_working()
        try:
            Switch.current_value = Switch.map_values.index(self.ecu.is_working())
            self.wiper.display()
        except:
            self.wash()

    @decorator_function
    def move_up(self):
        self.ecu.state = self.battery.is_working()
        if self.ecu.state != "off":
            self.wiper.state = self.ecu.is_working()
            self.switch.state = self.switch.move_up()
            self.ecu.state = self.switch.get_state()
            self.wiper.working = self.ecu.is_working()
            self.wiper.display()

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
        self.ecu.state = self.battery.is_working()
        if self.ecu.state != "off":
            self.wiper.state = self.ecu.is_working()
            self.switch.state = self.switch.move_down()
            self.ecu.state = self.switch.get_state()
            self.wiper.working = self.ecu.is_working()
            self.wiper.display()

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
        print(f"The switch mode  is {self.switch.get_state()}.".upper())
        print(f"The water  level is {self.watter_bottle.get_level()}.".upper())

    @decorator_function
    def wash(self):
        # self.check(self.switch.wash)
        self.ecu.state = self.battery.is_working()
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
