-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 30-Jun-2023 às 01:44
-- Versão do servidor: 10.4.24-MariaDB
-- versão do PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `social`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(30) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
--
-- Extraindo dados da tabela `posts`
--

INSERT INTO `posts` (`id`, `user_id`, `title`, `content`, `created_at`) VALUES
(1, 1, 'teste title', 'olá', '2023-06-28 11:28:27'),
(2, 1, 'teste title', 'teste', '2023-06-28 11:29:05'),
(3, 2, 'teste title', 'testeeee', '2023-06-28 11:41:57'),
(4, 2, 'teste title', 'teste teste teste testeteste', '2023-06-28 11:43:44'),
(5, 2, 'teste title', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', '2023-06-28 11:53:30'),
(6, 2, 'teste title', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget bibendum ante. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean accumsan arcu et massa vulputate facilisis. Suspendisse pretium nibh ut tortor cursus, at finibus mi dictum. Nulla facilisi. Donec fringilla libero vel ante finibus, eu aliquet arcu lobortis. Aliquam erat volutpat. Sed gravida mi et blandit faucibus. Ut sagittis, tortor non vestibulum facilisis, leo justo commodo velit, nec condimentum dolor mauris vitae arcu. Aenean luctus semper mi nec sagittis. Sed feugiat justo mattis, volutpat diam vel, dapibus dui. Ut sit amet metus purus. Nam mollis aliquam ipsum, blandit malesuada urna.\r\n\r\nMorbi eget molestie eros. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nulla eros sem, convallis id aliquam at, posuere eget nunc. Vivamus vitae justo tortor. Fusce id nibh sapien. Aliquam ac felis orci. Aliquam rutrum est urna, nec varius leo fermentum sed. Suspendisse nec iaculis dolor. Aliquam condimentum felis sit amet mi congue interdum. Praesent faucibus sapien mauris, vitae vestibulum arcu pretium non. Phasellus ut tincidunt arcu. Morbi commodo justo ex, vel egestas mi dictum ut. Nullam urna nibh, facilisis id congue nec, rhoncus vel nisl. Maecenas fermentum lacus et convallis commodo. Integer efficitur, lectus ut commodo consequat, metus sapien ullamcorper nibh, nec placerat ex felis iaculis nisi. Donec enim libero,', '2023-06-28 12:10:48'),
(7, 2, 'teste title', 'teste2', '2023-06-28 12:20:12');

-- --------------------------------------------------------

--
-- Estrutura da tabela `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(24) NOT NULL,
  `password` int(11) NOT NULL,
  `email` varchar(35) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'root', 123),
(2, 'root2', 123);

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices para tabela `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
