# Prim

A Python implementation on Prim's minimum spanning tree algorithm

## Getting Started

Download, clone or copy the code from the repository into a .py file

```

""" Example on how to setup and run the Prim's algorithm """
    # Initiates an instance of Prim's class
    p = Prim()
    
    # Add vertexes with any custom Label
    p.graph.add_vertexes(['A', 'B', 'C', 'D', 'E', 'F'])
    
    # Adds connections between the vertexes. Labels must match with already added vertexes
    p.graph.add_connections([
        ('A', 1, 'B'),
        ('A', 3, 'F'),
        ('A', 3, 'C'),
        ('B', 5, 'C'),
        ('B', 1, 'D'),
        ('C', 2, 'D'),
        ('C', 1, 'E'),
        ('D', 6, 'F'),
        ('E', 5, 'F')
    ])

    # Solves and returns a SpanningTree object, with all the information stored inside it
    minimum_spanning_tree = p.solve()
    print('Minimum Spanning Tree: \n')
    print(minimum_spanning_tree)

    
```

### Prerequisites

Python 3

## Running the tests

You can simply run the file to see the given output. The example is by the end of the file, and it starts on the function

```
if __name__ == '__main__':
```

## Contributing

Any contribution is very welcome to the project (Code, suggestions and even errors/bug reports). If you do wish to help, please contact me at: lucasbbr98@gmail.com


## Authors

* **Lucas Arruda Bonservizzi** - *Initial work* - [lucasbbr98](https://github.com/lucasbbr98)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspiration 1: I enjoyed an Operations Research class from professor Cleber Rocco at UNICAMP - FCA.
* Inspiration 2: Maybe my code can help someone around the world. 
* Feel free to contact me if you need any help at lucasbbr98@gmail.com.
