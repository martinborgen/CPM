# Origin
This project was conceived as a side project in university,
where this problem appeared in several project-management modules. 

# Use
The intended use is you get a .csv list where each task is on the form

"LABEL", "DURATION", "DEPENDENCY1", "DEPENDENCY2", ...

At the moment, the project is somewhere between initial working idea, and proper project. 

# TODO: 
* Organise source files, test files, etc. in some structure
* Re-work the CLI and/or finish an GUI
* Evaluate the current path-finding logic; it currently finds ALL possible paths which 
  risks becoming too slow and inefficient for large project-trees. 
* The current csv file usage cannot use headers, or the simple csv-reader will crash.
  It is probably a good idea to use a proper csv format, or something like pandas to 
  manage the task lists in the future.
* The current logic when entering a new task requires all dependencies to already be entered.
  It would be more flexible for the user if this wasn't necessary. A possible solution would 
  be to save dependencies not yet entered in a separate list and match those when they eventually
  are entered. 

Martin Borgén
2024-08-02