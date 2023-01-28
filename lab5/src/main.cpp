#include <random>
#include <vector>
#include <iostream>
#include <queue>
#include <thread>
#include <mutex>
#include <math.h>
#include <string>

#define THREADS 3

struct graph_t
{
    int size;
    int **matrix;
    int *neighbors_num;
    std::vector<std::string> description;
};

struct queues_t
{
    std::queue<graph_t> q1;
    std::queue<graph_t> q2;
    std::queue<graph_t> q3;
};

void count_neighbors(graph_t &graph)
{
    for (int i = 0; i < graph.size; i++)
    {
        int str_sum = 0;
        for (int j = 0; j < graph.size; j++)
        {
            str_sum += graph.matrix[i][j];
        }
        graph.neighbors_num[i] = str_sum;
    }
}

void make_description(graph_t &graph)
{
    for (int i = 0; i < graph.size; i++)
    {
        double color = double(graph.neighbors_num[i]) / graph.size * 0.4 + 0.6;

        graph.description.push_back("\t" + std::to_string(i + 1) + " [style=\"filled\", fillcolor=\"" + 
                                    std::to_string(color) + " 1.000 1.000\"]; \n");
        
        for (int j = i + 1; j < graph.size; j++)
        {
            if (graph.matrix[i][j] == 1)
                graph.description.push_back("\t" + std::to_string(i + 1) + " -- " + std::to_string(j + 1) + "; \n");
        }
    }
}

void write_to_file(graph_t &graph, int num)
{
    FILE *file = fopen(("output" + std::to_string(num) + ".dot").c_str(), "w");

    fprintf(file, "graph { \n");

    for (int i = 0; i < graph.description.size(); i++)
    {
        fprintf(file, graph.description[i].c_str());
    }

    fprintf(file, "}\n");

    fclose(file);

    // system("dot -Tpng graph.dot -o graph.png");
}


graph_t generate_graph(size_t size)
{
    graph_t result;

    result.size = size;

    result.matrix = new int* [result.size];
    for (int i = 0; i < result.size; i++)
    {
       (result.matrix)[i] = new int[result.size];
    }

    result.neighbors_num = new int[result.size];

    for (int i = 0; i < size; i++)
    {
        result.matrix[i][i] = 0;
        for (int j = i + 1; j < size; j++)
        {
            result.matrix[i][j] = rand() % 2;
            result.matrix[j][i] = result.matrix[i][j];
        }
    }

    return result;
}

double time_now = 0;

std::vector<double> t1;
std::vector<double> t2;
std::vector<double> t3;


void log_linear(graph_t &graph, int task_num, int stage_num, 
                void (*func)(graph_t &), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double start_res_time = time_now, res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(graph);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
               (time_end - time_start).count()) / 1e9;

    time_now = start_res_time + res_time;

    if (is_print)
        printf("Задача: %3d, Этап: %3d, Старт: %.6f, Конец: %.6f\n", 
               task_num, stage_num, start_res_time, start_res_time + res_time);
}

void log_linear(graph_t &graph, int task_num, int stage_num, 
                void (*func)(graph_t &, int), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double start_res_time = time_now, res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(graph, task_num);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
               (time_end - time_start).count()) / 1e9;

    time_now = start_res_time + res_time;

    if (is_print)
        printf("Задача: %3d, Этап: %3d, Старт: %.6f, Конец: %.6f\n", 
               task_num, stage_num, start_res_time, start_res_time + res_time);
}



void log_conveyor(graph_t &graph, int task_num, int stage_num, 
                  void (*func)(graph_t &), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(graph);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
               (time_end - time_start).count()) / 1e9;

    time_now += res_time;

    double start_res_time;

    if (stage_num == 1)
    {
        start_res_time = t1[task_num - 1];

        t1[task_num] = start_res_time + res_time;
        t2[task_num - 1] = t1[task_num];
    }
    else if (stage_num == 2)
    {
        start_res_time = t2[task_num - 1];

        t2[task_num] = start_res_time + res_time;
        t3[task_num - 1] = t2[task_num];
    }
    else if (stage_num == 3)
    {
        start_res_time = t3[task_num - 1];
    }

    if (is_print)
        printf("Задача: %3d, Этап: %3d, Старт: %.6f, Конец: %.6f\n", 
               task_num, stage_num, start_res_time, start_res_time + res_time);
}

void log_conveyor(graph_t &graph, int task_num, int stage_num, 
                  void (*func)(graph_t &, int), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(graph, task_num);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
               (time_end - time_start).count()) / 1e9;

    time_now += res_time;

    double start_res_time;

    if (stage_num == 1)
    {
        start_res_time = t1[task_num - 1];

        t1[task_num] = start_res_time + res_time;
        t2[task_num - 1] = t1[task_num];
    }
    else if (stage_num == 2)
    {
        start_res_time = t2[task_num - 1];

        t2[task_num] = start_res_time + res_time;
        t3[task_num - 1] = t2[task_num];
    }
    else if (stage_num == 3)
    {
        start_res_time = t3[task_num - 1];
    }

    if (is_print)
        printf("Задача: %3d, Этап: %3d, Старт: %.6f, Конец: %.6f\n", 
               task_num, stage_num, start_res_time, start_res_time + res_time);
}


void stage1_linear(graph_t &graph, int task_num, bool is_print)
{
    log_linear(graph, task_num, 1, count_neighbors, is_print);
}

void stage2_linear(graph_t &graph, int task_num, bool is_print)
{   
    log_linear(graph, task_num, 2, make_description, is_print);
}

void stage3_linear(graph_t &graph, int task_num, bool is_print)
{   
    log_linear(graph, task_num, 3, write_to_file, is_print);
}


void parse_linear(int count, size_t size, bool is_print)
{
    time_now = 0;

    std::queue<graph_t> q1;
    std::queue<graph_t> q2;
    std::queue<graph_t> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    for (int i = 0; i < count; i++)
    {
        graph_t res = generate_graph(size);
        
        queues.q1.push(res);
    }

    for (int i = 0; i < count; i++)
    {
        graph_t graph = queues.q1.front();
        stage1_linear(graph, i + 1, is_print);
        queues.q1.pop();
        queues.q2.push(graph);

        graph = queues.q2.front();
        stage2_linear(graph, i + 1, is_print); // Stage 2
        queues.q2.pop();
        queues.q3.push(graph);

        graph = queues.q3.front();
        stage3_linear(graph, i + 1, is_print); // Stage 3
        queues.q3.pop();
    }
}



void stage1_parallel(std::queue<graph_t> &q1, std::queue<graph_t> &q2, 
                    std::queue<graph_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    while(!q1.empty())
    {      
        m.lock();
        graph_t graph = q1.front();
        m.unlock();

        log_conveyor(graph, task_num++, 1, count_neighbors, is_print);

        m.lock();
        q2.push(graph);
        q1.pop();
        m.unlock();
    }
}


void stage2_parallel(std::queue<graph_t> &q1, std::queue<graph_t> &q2,
                     std::queue<graph_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    do
    {   
        m.lock();
        bool is_q2empty = q2.empty();
        m.unlock();

        if (!is_q2empty)
        {   
            m.lock();
            graph_t graph = q2.front();
            m.unlock();

            log_conveyor(graph, task_num++, 2, make_description, is_print);

            m.lock();
            q3.push(graph);
            q2.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty());
}


void stage3_parallel(std::queue<graph_t> &q1, std::queue<graph_t> &q2, 
                     std::queue<graph_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    do
    {
        m.lock();
        bool is_q3empty = q3.empty();
        m.unlock();

        if (!is_q3empty)
        {
            m.lock();
            graph_t graph = q3.front(); 
            m.unlock();

            log_conveyor(graph, task_num++, 3, write_to_file, is_print);

            m.lock();
            q3.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty() || !q3.empty());
}


void parse_parallel(int count, size_t size, bool is_print)
{
    time_now = 0;
    
    t1.resize(count + 1);
    t2.resize(count + 1);
    t3.resize(count + 1);

    for (int i = 0; i < count + 1; i++)
    {
        t1[i] = 0;
        t2[i] = 0;
        t3[i] = 0;
    }

    std::queue<graph_t> q1;
    std::queue<graph_t> q2;
    std::queue<graph_t> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    
    for (int i = 0; i < count; i++)
    {
        graph_t res = generate_graph(size);
        
        q1.push(res);
    }

    std::thread threads[THREADS];

    threads[0] = std::thread(stage1_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[1] = std::thread(stage2_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[2] = std::thread(stage3_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);

    for (int i = 0; i < THREADS; i++)
    {
        threads[i].join();
    }

}

void print_menu()
{
    std::cout << "1. Линейная обработка \n2. Конвейерная обработка \n0. Выход\n\n" << std::endl;
}


void run()
{
    int option = -1;

    while (option != 0)
    {
        print_menu();

        std::cout << "Выбор: ";
        std::cin >> option;

        int size, count;

        if (option > 0 & option < 3)
        {
            std::cout << "\n\nРазмер графа: ";
            std::cin >> size;

            std::cout << "Количество графов: ";
            std::cin >> count;

            if (option == 1)
                parse_linear(count, size, true);
            else
                parse_parallel(count, size, true);

            std::cout << "\n";

        }
        else if (option < 0 || option > 2)
        {
            std::cout << "\nОшибка: Неверно введен пункт меню. Повторите\n" << std::endl;
        }
    }
}



int main(void)
{
    run();

    return 0;
}
