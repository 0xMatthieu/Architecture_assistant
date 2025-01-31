from ai_agent import call_agent


if __name__ == "__main__":
    print("start")
    debug = False

    if debug:
        print("debug started")
        #start server first with python -m phoenix.server.main serve
        #more info at https://huggingface.co/docs/smolagents/tutorials/inspect_runs
        from telemetry import use_telemetry
        use_telemetry()

    #call_agent(query=f'what would be best solution for 4 DO and 3 PWM, 2x CAN in Codesys ?',
    #           ui=False)
    print("---------------- \n next test \n")
    call_agent(query=f'what would be best solution for 4 DO and 38 PWM, 7x CAN in Codesys ?. Provide offer as well',
               ui=False)
    print("done")
