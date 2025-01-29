from ai_agent import call_agent

if __name__ == "__main__":
    print("start")
    #call_agent(query=f'what would be best solution for 4 DO and 3 PWM, 2x CAN in Codesys ?',
    #           simple_agent=False)
    print("---------------- \n next test \n")
    call_agent(query=f'what would be best solution for 4 DO and 38 PWM, 7x CAN in Codesys ?',
               simple_agent=False)
    print("done")
