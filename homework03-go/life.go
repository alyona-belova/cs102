package main

import (
	"bufio"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

type GameOfLife struct {
	rows            int
	cols            int
	generations     int
	maxGenerations  int
	prevGenerations [][]int
	currGenerations [][]int
}

type Cell struct {
	row int
	col int
}

//CreateGrid creates grid
func CreateGrid(rows int, cols int, randomize bool) [][]int {
	grid := make([][]int, rows)
	for i := 0; i < rows; i++ {
		grid[i] = make([]int, cols)
		if randomize == true {
			for j := 0; j < cols; j++ {
				grid[i][j] = rand.Intn(2)
			}
		}
	}
	return grid
}

//GetNeighbours gets neighbours
func (game *GameOfLife) GetNeighbours(cell Cell) []int {
	result := make([]int, 0)
	row, col := cell.row, cell.col
	if col > 0 {
		result = append(result, game.currGenerations[row][col-1])
	}
	if col < game.cols-1 {
		result = append(result, game.currGenerations[row][col+1])
	}
	if row > 0 {
		result = append(result, game.currGenerations[row-1][col])
		if col > 0 {
			result = append(result, game.currGenerations[row-1][col-1])
		}
		if col < game.cols-1 {
			result = append(result, game.currGenerations[row-1][col+1])
		}
	}
	if row < game.rows-1 {
		result = append(result, game.currGenerations[row+1][col])
		if col > 0 {
			result = append(result, game.currGenerations[row+1][col-1])
		}
		if col < game.cols-1 {
			result = append(result, game.currGenerations[row+1][col+1])
		}
	}
	return result
}

//GetNextGeneration gets next generation
func (game *GameOfLife) GetNextGeneration() [][]int {
	alive := make([]Cell, 0)
	dead := make([]Cell, 0)
	for i := 0; i < game.rows; i++ {
		for j := 0; j < game.cols; j++ {
			game.prevGenerations[i][j] = game.currGenerations[i][j]
		}
	}
	for i := 0; i < game.rows; i++ {
		for j := 0; j < game.cols; j++ {
			neighbours := game.GetNeighbours(Cell{i, j})
			sum := 0
			for _, i := range neighbours {
				sum += i
			}
			if sum < 2 || sum > 3 {
				dead = append(dead, Cell{i, j})
			} else if sum == 3 && game.currGenerations[i][j] == 0 {
				alive = append(alive, Cell{i, j})
			}
		}
	}
	for _, i := range alive {
		game.currGenerations[i.row][i.col] = 1
	}
	for _, i := range dead {
		game.currGenerations[i.row][i.col] = 0
	}
	return game.currGenerations
}

//Step completes one step of the game
func (game *GameOfLife) Step() {
	game.GetNextGeneration()
	game.generations++
}

//IsMaxGenerationsExceeded checks whether the current number of generations has exceeded the maximum
func (game *GameOfLife) IsMaxGenerationsExceeded() bool {
	if game.generations >= game.maxGenerations {
		return true
	}
	return false
}

//IsChanging checks whether the state of the cells has changed since the previous step
func (game *GameOfLife) IsChanging() bool {
	for i := 0; i < game.rows; i++ {
		for j := 0; j < game.cols; j++ {
			if game.currGenerations[i][j] != game.prevGenerations[i][j] {
				return true
			}
		}
	}
	return false
}

//FromFile reads the state of cells from the specified file
func FromFile(filename string) GameOfLife {
	var grid [][]int
	file, _ := os.Open(filename)
	defer file.Close()
	reader := bufio.NewReader(file)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		strArray := strings.Split(strings.Trim(line, "\n"), "")
		var intArray []int
		for _, str := range strArray {
			temp, _ := strconv.ParseInt(str, 10, 64)
			intArray = append(intArray, int(temp))
		}
		grid = append(grid, intArray)
	}
	game := GameOfLife{
		rows:            len(grid),
		cols:            len(grid[0]),
		prevGenerations: CreateGrid(len(grid), len(grid[0]), false),
		currGenerations: CreateGrid(len(grid), len(grid[0]), false),
		maxGenerations:  1000,
		generations:     1,
	}
	game.currGenerations = grid
	return game
}

//Save saves the current state of cells to the specified file
func (game *GameOfLife) Save(filename string) {
	file, _ := os.Create(filename)
	writer := bufio.NewWriter(file)
	defer file.Close()
	for _, row := range game.currGenerations {
		var strResult string
		for _, i := range row {
			strResult += strconv.Itoa(i)
		}
		writer.WriteString(strResult + "\n")
	}
	writer.Flush()
}

func main() {
	game := FromFile("grid.txt")
	for i := 0; i < 3; i++ {
		game.Step()
	}
	game.Save("currGeneration.txt")
}
