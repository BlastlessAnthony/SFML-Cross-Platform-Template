#include <SFML/Graphics.hpp>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    sf::RenderWindow *window = new sf::RenderWindow(sf::VideoMode(1024, 768, 32), "SFML Window", sf::Style::Default);
    sf::Event sfml_event;

    window->setFramerateLimit(60);
    while (window->isOpen())
    {
        while (window->pollEvent(sfml_event)) {
            switch (sfml_event.type) {
                case sf::Event::Closed: window->close(); break;
                case sf::Event::Resized: printf("Window was resized to [%dx%d].", window->getSize().x, window->getSize().y); break;
                case sf::Event::LostFocus: printf("Window lost focus."); break;
                case sf::Event::GainedFocus: printf("Window gained focus.");
                default: break;
            }
        }

        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Escape)) {window->close();}
    }
    return (EXIT_SUCCESS);
}