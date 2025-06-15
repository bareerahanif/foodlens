from dotenv import load_dotenv
load_dotenv()  
from model_context import ModelContext

def main():
    ctx = ModelContext()

    while True:
        print("\n=== Available Models ===")
        ctx.list_models()
        choice = input("Select a model (1-3) or type 'exit' to quit: ").strip()

        if choice.lower() == "exit":
            print("Goodbye!")
            break

        if not ctx.switch_model(choice):
            continue

        while True:
            print(f"\n[Current Model: {ctx.get_current_model_name()}]")
            query = input("Enter your natural language query (or type 'switch' to change model, 'exit' to quit): ").strip()

            if query.lower() == "exit":
                print("Goodbye!")
                return
            elif query.lower() == "switch":
                break
            elif query == "":
                continue
            else:
                sql = ctx.process_query(query)
                print(f"\n[SQL Output]\n{sql}")

if __name__ == "__main__":
    main()
