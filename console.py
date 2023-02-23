from rich.console import Console
console = Console()

def error(*arg):
    arg = list(arg)
    console.log("[red][ERROR] [/red]"+" ".join([str(i) for i in arg]))

def warn(*arg):
    arg = list(arg)
    console.log("[yellow][WARN] [/yellow]"+" ".join([str(i) for i in arg]))

def log(*arg):
    arg = list(arg)
    console.log("[LOG] "+" ".join([str(i) for i in arg]))

print = console.print
status = console.status