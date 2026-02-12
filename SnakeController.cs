using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class SnakeController : MonoBehaviour
{
    public GameObject segmentPrefab;
    public GameObject headPrefab;
    public float moveInterval = 0.2f;
    public int startLength = 3;
    public int gridWidth = 10;
    public int gridHeight = 10;
    public bool teleportThroughWalls = true;
    public TextMeshProUGUI scoreText;
    
    private List<Transform> segments = new List<Transform>();
    private Vector2 direction = Vector2.up;
    private Vector2 nextDirection = Vector2.up;
    private float timer;
    private bool ateFood = false;
    private int score = 0;
    
    void Start()
    {
        ResetSnake();
    }
    
    void Update()
    {
        if (Input.GetKey(KeyCode.UpArrow) || Input.GetKey(KeyCode.W))
        {
            if (direction != Vector2.down)
                nextDirection = Vector2.up;
        }
        else if (Input.GetKey(KeyCode.DownArrow) || Input.GetKey(KeyCode.S))
        {
            if (direction != Vector2.up)
                nextDirection = Vector2.down;
        }
        else if (Input.GetKey(KeyCode.LeftArrow) || Input.GetKey(KeyCode.A))
        {
            if (direction != Vector2.right)
                nextDirection = Vector2.left;
        }
        else if (Input.GetKey(KeyCode.RightArrow) || Input.GetKey(KeyCode.D))
        {
            if (direction != Vector2.left)
                nextDirection = Vector2.right;
        }
        
        timer += Time.deltaTime;
        if (timer >= moveInterval)
        {
            timer = 0;
            direction = nextDirection;
            Move();
        }
    }
    
    void Move()
    {
        Vector2 prevPos = segments[0].position;
        Vector2 newPos = prevPos + direction;
        
        if (teleportThroughWalls)
        {
            if (newPos.x > gridWidth)
                newPos.x = -gridWidth;
            else if (newPos.x < -gridWidth)
                newPos.x = gridWidth;
                
            if (newPos.y > gridHeight)
                newPos.y = -gridHeight;
            else if (newPos.y < -gridHeight)
                newPos.y = gridHeight;
        }
        
        segments[0].position = newPos;
        
        for (int i = 1; i < segments.Count; i++)
        {
            Vector2 tempPos = segments[i].position;
            segments[i].position = prevPos;
            prevPos = tempPos;
        }
        
        if (ateFood)
        {
            GrowSnake(prevPos);
            ateFood = false;
        }
        
        CheckSelfCollision();
    }
    
    void GrowSnake(Vector2 position)
    {
        GameObject newSegment = Instantiate(segmentPrefab, position, Quaternion.identity);
        segments.Add(newSegment.transform);
    }
    
    void CheckSelfCollision()
    {
        Vector2 headPos = segments[0].position;
        
        for (int i = 1; i < segments.Count; i++)
        {
            if ((Vector2)segments[i].position == headPos)
            {
                ResetSnake();
                break;
            }
        }
    }
    
    void ResetSnake()
    {
        foreach (Transform seg in segments)
        {
            if (seg != null)
                Destroy(seg.gameObject);
        }
        segments.Clear();
        
        score = 0;
        if (scoreText != null)
            scoreText.text = "Счёт: 0";
        
        GameObject head = Instantiate(headPrefab, Vector3.zero, Quaternion.identity);
        segments.Add(head.transform);
        
        for (int i = 1; i < startLength; i++)
        {
            GameObject segment = Instantiate(segmentPrefab, new Vector3(0, -i, 0), Quaternion.identity);
            segments.Add(segment.transform);
        }
        
        direction = Vector2.up;
        nextDirection = Vector2.up;
        timer = 0;
        
        GameObject[] oldFood = GameObject.FindGameObjectsWithTag("Food");
        foreach (GameObject food in oldFood)
            Destroy(food);
            
        FindObjectOfType<FoodSpawner>().SpawnFood();
    }
    
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.tag == "Food")
        {
            ateFood = true;
            Destroy(other.gameObject);
            
            score += 10;
            if (scoreText != null)
                scoreText.text = "Счёт: " + score;
            
            FindObjectOfType<FoodSpawner>().SpawnFood();
            
            if (score % 50 == 0 && moveInterval > 0.05f)
            {
                moveInterval -= 0.02f;
            }
        }
        
        if (other.tag == "Wall" && !teleportThroughWalls)
        {
            ResetSnake();
        }
    }
}