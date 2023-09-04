# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class PVector:
    def __init__(self, ):


def parse(strin: str):
    end = strin.find("UrQMD")
    st = end
    while st >= 0:
        st = end
        end = strin.find("UrQMD", st + 1)
        parse_event(strin[st:end])


def parse_event(strin: str):
    for line in strin.splitlines()[1:]:
        for word in line.split(" "):
            print(word)


if __name__ == "__main__":
    parse("UrQMD asd qwdqwd qwd dqwd\n"
                "data1 data2 data3\n"
                "UrQMD  2 12e 21d12d   12e d\t \n"
                "data4 data5 data6\n")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
