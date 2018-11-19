from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


class NewVisitorTest(FunctionalTest):

	def test_case_start_a_list_for_one_user(self):
		# Edith ouviu falar de um novo aplicativo de tarefas on-line. Ela vai
		# para verificar sua página inicial
		self.browser.get(self.live_server_url)

        # Ela percebe que o título da página e o cabeçalho mencionam listas de tarefas
		self.assertIn ('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# Ela é convidada a inserir um item de tarefa imediatamente
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		# Ela digita "Compre penas de pavão" em uma caixa de texto (o passatempo de Edith
        # está amarrando iscas de pesca com mosca)
		inputbox.send_keys('Buy peacock feathers')

		# Quando ela acerta, a página é atualizada e agora a página lista
        # "1: Compre penas de pavão" como um item em uma tabela de lista de tarefas pendentes
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# Ainda há uma caixa de texto convidando-a para adicionar outro item. Ela
        # entra "Use penas de pavão para fazer uma mosca" (Edith é muito
        # metódico)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# A página é atualizada novamente e agora mostra os dois itens da lista dela
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		# Satisfeito, ela volta a dormir

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Edith inicia uma nova lista de tarefas
		self.browser.get(self.live_server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# Ela percebe que sua lista tem um URL exclusivo
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')


        # Agora, um novo usuário, Francis, vem ao site.

        # # Usamos uma nova sessão do browser para garantir que nenhuma informação
        # # de Edith está vindo de cookies etc

		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visita a página inicial. 
		#Não há sinal de Edith
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

 		# Francis inicia uma nova lista digitando um novo item. Ele
        # é menos interessante que Edith ...
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		
		# Francis recebe seu próprio URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# Novamente, não há nenhum vestígio da lista de Edith
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Satisfeito, ambos voltam a dormir

