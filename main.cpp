#include <raylib.h>
#include <iostream>

using namespace std;

int player_score = 0;
int ai_score = 0;

class Ball {
public:
	float x, y;
	int speed_x, speed_y;
	int radius;
	void Draw() {
		DrawCircle(x, y, radius, DARKBLUE);
}
	void update() {
		x += speed_x;
		y += speed_y;
		if (y + radius >= GetScreenHeight() || y - radius <= 0)
		{
			speed_y *= -1;
		}
		if (x + radius >= GetScreenWidth())
		{
			player_score++;
			ResetBall();
			WaitTime(1.0f);
		}
		if (x - radius <= 0)
		{
			ai_score++;
			ResetBall();
			WaitTime(1.0f);
		}
	}
	void ResetBall() {
		x = GetScreenWidth() / 2;
		y = GetScreenHeight() / 2;
		int speed_choices[2] = { -1,1 };
		speed_x *= speed_choices[GetRandomValue(0, 1)];
		speed_y *= speed_choices[GetRandomValue(0, 1)];

	}
};

class Paddle {
protected:
	void LimitMovement() {
		if (y <= 0)
		{
			y = 0;
		}
		if (y + height >= GetScreenHeight())
		{
			y = GetScreenHeight() - height;
		}
	}

public:
float x, y;
float width,height;
int speed;
void Draw() 
{
	DrawRectangle(x,y,width,height, DARKBLUE);
}
void update() {
	if (IsKeyDown(KEY_UP))
	{
		y = y - speed;
	}
	if (IsKeyDown(KEY_DOWN))
	{
		y = y + speed;
	}
	LimitMovement();
}
};
class CPUPaddle : public Paddle {
public:
	void Update(int ball_y)
	{
		if (y + height / 2 > ball_y)
		{
			y = y - speed;
		}
		if (y + height / 2 <= ball_y)
		{
			y = y + speed;
		}
		LimitMovement();
	}
};

Ball ball;
Paddle player;
CPUPaddle AI;


int main()
{
	const int screen_width = 1280;
	const int screen_height = 800;
	InitWindow(screen_width, screen_height, "Pong");
	SetTargetFPS(144);

	ball.radius = 20;
	ball.x = screen_width / 2;
	ball.y = screen_height / 2;
	ball.speed_x = 4;
	ball.speed_y = 4;


	player.width = 25;
	player.height = 120;
	player.x = 10;
	player.y = screen_height / 2 - player.height / 2;
	player.speed = 3;


	AI.height = 120;
	AI.width = 25;
	AI.x = screen_width - AI.width - 10;
	AI.y = screen_height / 2 - AI.height / 2;
	AI.speed = 3;

	while (WindowShouldClose() == false)
	{
	
		BeginDrawing();
		ClearBackground(SKYBLUE);
		ball.update();
		player.update();
		AI.Update(ball.y);
		if (CheckCollisionCircleRec(Vector2{ ball.x,ball.y }, ball.radius, Rectangle{ player.x,player.y,player.width,player.height }))
		{
			ball.speed_x *= -1;
		}
		if (CheckCollisionCircleRec(Vector2{ ball.x,ball.y }, ball.radius, Rectangle{ AI.x,AI.y,AI.width,AI.height }))
		{
			ball.speed_x *= -1;
		}

		DrawLine(screen_width / 2, 0, screen_width / 2, screen_height, DARKBLUE);
		DrawCircle(GetScreenWidth() / 2, GetScreenHeight() / 2, 120, BLUE);
		ball.Draw();
		AI.Draw();
		player.Draw();
		DrawText(TextFormat("%i", player_score), screen_width / 4 - 20, 20, 80, DARKBLUE);
		DrawText(TextFormat("%i", ai_score), 3*screen_width / 4 - 20, 20, 80, DARKBLUE);
		EndDrawing();
	}
	CloseWindow();
}