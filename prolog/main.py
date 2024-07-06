from knowledge.interpreter import Interpreter
from knowledge.interpreter import Interpreter
from knowledge.expr import Expr
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
console = Console()
kn = Interpreter("sdf")

def main():
    console.clear()
    console.print("Welcome to the Prolog Interpreter", style="bold magenta")
    # while True:
    #     text = console.input("[bold red]>>>[/] ")
    #     if text == "q":
    #         break
    # console.print(Panel(Pretty("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis mattis accumsan eros, id pulvinar mauris scelerisque sit amet. Aenean eu venenatis purus. Aliquam sem libero, vehicula vel auctor a, auctor in neque. Ut id orci ornare, ultricies turpis ut, pulvinar lacus. In a felis auctor, egestas est at, viverra diam. In auctor rhoncus lectus quis semper. Maecenas eget sagittis elit. Maecenas et nibh et tellus aliquam semper. Fusce sed ligula nisl. Nullam ultricies, purus non lacinia tempus, sem sapien pellentesque odio, at consequat urna arcu non erat.")))
    while True:
        # text = console.input("[bold green]>>> [/]")
        query = Prompt.ask("[bold cyan]prolog>[/bold cyan]")
        if query.lower() in ['quit', 'exit']:
            console.print("Exiting Prolog Interpreter. Goodbye!", style="bold red")
            break
        if "?" in query:
            output = kn.query(Expr(query.replace("?", "")))
            # console.rule()
            table = Table(show_header=True, header_style="bold green")
            table.add_column("Query", style="dim", width=30)
            table.add_column("Result", style="bold yellow")

            table.add_row(query, str(output))
        
            console.print(table)
        else:
            kn([query])
    # kn.add_kn("Father(ali, nima)")
    # kn.add_kn("Father(ali, hossein)")
    # x = Expr("Father(X, nima)")
    # console.print(x)
    # an = kn.query(Expr("Father(X1, nima)"))
    # console.print(an)
    #kn.add_kn([
    #    "Father(mahdi, ali)",
    #    "Mother(mahdi, ali)",
    #    "Father(Hesam , ali)"
    #])
    # kn.add_kn("Father(X, Y) :- Mother(X, Z), Father(Y, Z)")
    #answer = kn.query(Expr("Father(Q, D)?".replace("?", "")))
    #console.print(answer)
    # console.print(answer)
   


if __name__ == "__main__":
    main()