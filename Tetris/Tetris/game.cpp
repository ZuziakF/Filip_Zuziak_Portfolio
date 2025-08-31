#include "game.h"
#include <random>
Game::Game()
{
	grid = Grid();
	blocks = GetAllBlocks();
	currentBlock = GetRandomBlock();
	nextBlock = GetRandomBlock(); 
	GameOver = false;
	score = 0;
	InitAudioDevice();
	music = LoadMusicStream("Music/music.mp3");
	PlayMusicStream(music);
	rotateSound = LoadSound("Music/rotate.mp3");
	clearSound = LoadSound("Music/clear.mp3");
}

Game::~Game()
{
	UnloadSound(rotateSound);
	UnloadSound(clearSound);
	UnloadMusicStream(music);
	CloseAudioDevice();
}
Block Game::GetRandomBlock()
{
	if (blocks.empty())
	{
		blocks = GetAllBlocks();
	}
	int randomIndex = rand() % blocks.size();
	Block block = blocks[randomIndex];
	blocks.erase(blocks.begin() + randomIndex);
	return block;
}

vector<Block> Game::GetAllBlocks()
{
		return { IBlock(),JBlock(),LBlock(),OBlock(),SBlock(),TBlock(),ZBlock() };
}
void Game::Draw()
{
	grid.Draw();
	currentBlock.Draw(11,11);
	switch (nextBlock.id)
	{
	case 3:
		nextBlock.Draw(255, 290);
		break;
	case 4:
		nextBlock.Draw(255, 280);
		break;
	default:
		nextBlock.Draw(270, 270);
		break;
	}
}
void Game::HandleInput()
{
	int keyPressed = GetKeyPressed();
	if (GameOver && keyPressed != 0)
	{
		GameOver = false;
		Reset();
	}
	switch (keyPressed)
	{
	case KEY_LEFT:
		MoveBlockLeft();
		break;

	case KEY_RIGHT:
		MoveBlockRight();
		break;
	case KEY_DOWN:
		MoveBlockDown();
		updateScore(0, 1);
		break;
	case KEY_UP:
		RotateBlock();
		break;
	}

}

void Game::MoveBlockLeft()
{
	if (!GameOver) 
	{
		currentBlock.Move(0, -1);
		if (IsBlockOutside() || BlockFits() == false)
		{
			currentBlock.Move(0, 1);
		}
	}
}
void Game::MoveBlockRight()
{
	if (!GameOver) 
	{
			currentBlock.Move(0, 1);
			if (IsBlockOutside() || BlockFits() == false)
			{
				currentBlock.Move(0, -1);
			}
	}
}
void Game::MoveBlockDown()
{
	if (!GameOver)
	{
		currentBlock.Move(1, 0);
		if (IsBlockOutside() || BlockFits() == false)
		{
			currentBlock.Move(-1, 0);
			LockBlock();
		}
	}
}

bool Game::IsBlockOutside()
{
	vector<Position> tiles = currentBlock.GetCellPositions();
	for (Position item : tiles)
	{
		if (grid.IsCellOutside(item.row, item.column))
		{
			return true;
		}
	}
	return false;
}
void Game::RotateBlock()
{
	if (!GameOver) 
	{
		currentBlock.Rotate();
		if (IsBlockOutside())
		{
			currentBlock.UndoRotation();
		}
		else
		{
			PlaySound(rotateSound);
		}
	}
}
void Game::LockBlock() 
{
	vector<Position> tiles = currentBlock.GetCellPositions();
	for (Position item : tiles)
	{
		grid.grid[item.row][item.column] = currentBlock.id;
	}
	currentBlock = nextBlock;
	if (BlockFits() == false)
	{
		GameOver = true;
	}
	nextBlock = GetRandomBlock();
	int rowsCleared=grid.ClearFullRows(); 
	if (rowsCleared > 0) 
	{
		PlaySound(clearSound);
		updateScore(rowsCleared, 0);
	}
}
bool Game::BlockFits()
{
	vector<Position> tiles = currentBlock.GetCellPositions();
	for (Position item : tiles)
	{
		if (grid.IsCellEmpty(item.row, item.column) == false)
		{
			return false;
		}

	}
	return true;
}

void Game::Reset()
{
	grid.Initialize();
	blocks = GetAllBlocks();
	currentBlock = GetRandomBlock();
	nextBlock = GetRandomBlock();
	score = 0;

}
void Game::updateScore(int linesCleared, int moveDownPoints)
{
	switch (linesCleared)
	{
	case 1:
		score += 100;
		break;
	case 2:
		score += 300;
		break;
	case 3:
		score += 500;
		break;
	default:
		break;
	}

	score+=moveDownPoints;
}
