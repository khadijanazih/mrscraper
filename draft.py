from playwright.sync_api import sync_playwright
import datetime
def clean_editions(start_time=None, end_time=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path=CHROME_PATH)
        context = browser.new_context(storage_state="state.json", ignore_https_errors=True)
        context.set_default_navigation_timeout(300000)
        page = context.new_page()
        page.goto("https://waterp-cas.srm-cas.local")
        page.wait_for_selector("#editions ul li a.dashmod__editions--close", timeout=50000)
        editions = page.evaluate("document.querySelectorAll('a.dashmod__editions--close').length")
        print(editions)
        context.close()
        browser.close()
def print_editions(start_time=None, end_time=None): # No change needed here if it doesn't call set_info_msgs
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path=CHROME_PATH)
        context = browser.new_context(storage_state="state.json",
                                      ignore_https_errors=True, accept_downloads= True)
        context.set_default_navigation_timeout(12000000)
        page = context.new_page()
        page.goto("https://waterp-cas.srm-cas.local")
        page.wait_for_selector("#editions ul li")

        first_time_span = page.locator("#editions ul li:first-child span.dashmod__editions--date").inner_text()
        page.wait_for_load_state("domcontentloaded")
        last_time_span = page.locator("#editions ul li:last-child span.dashmod__editions--date").inner_text()
        editions =  page.locator("#editions ul li")
        editions_count = editions.count()
        first_time = ' '.join(first_time_span.split())
        last_time = ' '.join(last_time_span.split())
        for i, edition in enumerate(editions.all()):
            page.wait_for_timeout(5000)
            edition_date = edition.locator("span.dashmod__editions--date").inner_text()
            formatted_edition_date = ' '.join(edition_date.split())
            if start_time <= formatted_edition_date <= end_time:
                with page.expect_download() as download_info:
                    edition.locator(".dashmod__editions--link").click()
                    download = download_info.value
                    download.save_as(f"C:\\Users\\star1\\Downloads\\{download.suggested_filename}") # Removed redundant download var
        browser.close()
def process_factures(self, factures, print_logo = False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path=CHROME_PATH)
        context = browser.new_context(storage_state="state.json", ignore_https_errors=True)
        context.set_default_navigation_timeout(60000)
        page = context.new_page()
        page.goto("https://waterp-cas.srm-cas.local/reporting/report")
        page.wait_for_load_state("domcontentloaded")
        page.click('.reportingnav--types > li > a:has-text("Facturation")')
        page.wait_for_load_state("domcontentloaded")

        total_factures = len(factures)
        for i, facture in enumerate(factures):

            if i == 0 : start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if facture[1].startswith("BT "):

                page.click("div#reportDoc_FCEP200U_waterp_client_cas_cas > a")
                page.fill('input[id$="NUM_FAC_CLI"]', facture[0])
                page.wait_for_load_state("domcontentloaded")
                if print_logo:
                    page.fill('input[id$="P_Logo"]', 'O')
                    print(f"{facture[1]} basse {print_logo}")
                else: page.fill('input[id$="P_Logo"]', '')

                page.click("browse_button[id ='browse_button-FCEP200U_waterp_client_cas_cas']")
                page.wait_for_timeout(2000)
                page.click("div#reportDoc_FCEP200U_waterp_client_cas_cas > a")

            elif facture[1].startswith("MT "):
                page.click("div#reportDoc_FCEP200U_MT_waterp_client_cas_cas > a")
                page.fill('input[id$="num_fac_cli"]', facture[0])
                page.wait_for_load_state("domcontentloaded")
                if print_logo:
                    print("with logo bt")
                    page.fill('input[id$="P_Logo"]', 'O')
                else: page.fill('input[id$="P_Logo"]', '')
                page.click("browse_button[id ='browse_button-FCEP200U_MT_waterp_client_cas_cas']")
                page.wait_for_timeout(2000)
                page.click("div#reportDoc_FCEP200U_MT_waterp_client_cas_cas > a")
                self.progress_title.configure(text=f"Traitement en cours : {i+1} / {len(factures)}")
                self.progress_title.update()

                self.progress_value.configure(text=f"{((i + 1) / len(factures))*100}%")
                self.progress_value.update()
                self.master.update_idle_tasks()
                set_info_msgs(self, 'info', f'Traitement en cours : {i+1} / {len(factures)} | ({((i + 1) / len(factures))*100}%)')
                self.master.update()
            if   i == len(factures) - 1 : end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        set_info_msgs(self, 'info', f'start_time: {start_time} \n end_time: {end_time}')
        set_info_msgs(self, 'info', f'{len(factures)} proccessed')
        browser.close()
    return True, start_time, end_time
def  process_contrats(self, contrats):
    fetched_data_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path=CHROME_PATH)
        context = browser.new_context(storage_state="state.json", ignore_https_errors=True)
        context.set_default_navigation_timeout(60000)
        page = context.new_page()
        for contrat in contrats:
            try:
                page.goto(fr'https://waterp-cas.srm-cas.local/clientele/synthese/contrat/{contrat}')#lien irl = synthese/contrat/NUM_CONTRAT
                page.wait_for_load_state('domcontentloaded')
                page.click('a[data-target="#compteclient"]')
                page.wait_for_load_state("load")
                empty_solde = page.locator('#compteclient .search-noresult')
                solde_span = page.locator("#toolbar #btns-action .item-bloc-stat span:has-text('Factures') + strong .solde-price")
                if empty_solde.is_visible() and not solde_span.is_visible():
                    print(f"le contrat {contrat} n'a Aucune Facture ")
                    set_info_msgs(self, 'info', f"le contrat {contrat} n'a Aucune Facture")
                    print("__________________________________________________")
                    continue
                solde_val = solde_span.text_content()
                solde_val = clean_price_spans(solde_val)
                invoice_blocks = page.locator('#blocNC1 .hpanel')
                solde_span_color = solde_span.evaluate('el=> window.getComputedStyle(el).color')
                solde_type_text = "Accompte de -" if solde_span_color == 'rgb(120, 163, 0)' else "Montant Impayé de "
                print(f"le contrat : {contrat} a un {solde_type_text}{solde_val} DHS")
                set_info_msgs(self, 'info', f"le contrat : {contrat} a un {solde_type_text}{solde_val} DHS")
                print("__________________________________________________")

                for i in range(invoice_blocks.count()):
                    invoice_block = invoice_blocks.nth(i)
                    fetched_data = {}
                    num_fact_handle = invoice_block.locator('.panel-body .text-muted a')
                    num_fact_handle =  num_fact_handle.inner_text() if num_fact_handle.count() > 0 else None
                    montant_handle = invoice_block.locator('.panel-footer .row > div:first-child > .item-bloc-stat strong')
                    montant_handle = clean_price_spans(montant_handle.inner_text()) if montant_handle.count() > 0 else None
                    echeance_handle = invoice_block.locator('.panel-footer .row > div:nth-child(4) > .item-bloc-stat strong')
                    echeance_handle = echeance_handle.inner_text() if echeance_handle.count() > 0 else None
                    if echeance_handle !="-" and echeance_handle != None:
                        echeance_handle = datetime.strptime(echeance_handle, "%d/%m/%Y")
                        echeance_status = "" if echeance_handle > datetime.today() else "E"
                        echeance_handle = echeance_handle.strftime("%d-%m-%Y")
                    else:
                        echeance_handle = "-"
                        echeance_status = ""
                    pns_handle = invoice_block.locator('.panel-body .solde-price')
                    if pns_handle.count() > 0:
                        is_negative = pns_handle.evaluate("el=>el.classList.contains('negative')")
                        pns_handle = clean_price_spans(pns_handle.inner_text())
                        statut ="NR" if is_negative else ""
                    fetched_data ['Contrat'] = contrat
                    fetched_data ['Facture'] = num_fact_handle
                    fetched_data ['Montant'] = montant_handle
                    fetched_data ['Echéance'] = echeance_handle
                    fetched_data ['MontantExegible'] = pns_handle
                    fetched_data ['Statut'] = statut
                    fetched_data ['Statut Echéance'] = echeance_status
                    fetched_data_list.append(fetched_data)
                    self.progress_value.configure(text=f"{((i + 1) / len(contrats)) * 100}%")
                    self.master.update_idle_tasks()

            except TargetClosedError as e:
                set_info_msgs(self, 'alert', f'Navigateur Fermé, avant de traiter le contrat {contrat} : \n Erreur : {e}')

            except TimeoutError as e:
                set_info_msgs(self, 'alert', f'Délai d\'attente Dépassé pour le contrat {contrat} : \n Erreur : {e}')
                continue

            except Error as e:
                set_info_msgs(self, 'alert', f'Erreur d\'extraction Serveur pour le contrat {contrat} : \n Erreur : {e}')
                continue

            except (AttributeError, TypeError) as e:
                set_info_msgs(self, 'alert', f'Erreur de traitement de données pour le contrat {contrat} : \n Erreur : {e}')
                continue

            except ValueError as e:
                set_info_msgs(self, 'alert', f'Erreur de conversion de données pour le contrat {contrat} : \n Erreur : {e}')
                continue

            except Exception as e:
                set_info_msgs(self, 'alert', f'Erreur Inconnue pour le contrat {contrat} : \n Erreur : {e}')
                continue

        # Clean up
        if browser: browser.close()
        if p: p.stop()
        set_info_msgs(self, 'info', f"Données de {len(contrats)} contrats extraites")

    return fetched_data_list
def execute(self, check_value = None):
    if isinstance(self.extracted_data, list) and len(self.extracted_data) > 0:
        print('after state')
        # Check if it's an array of tuples
        if all(isinstance(item, tuple) and len(item) == 2 for item in self.extracted_data):
            set_info_msgs(self, 'info', 'Array of tuples detected')
            print("Array of tuples detected")
            return process_factures(self, self.extracted_data, check_value)

        # Check if it's a simple array of strings
        elif all(isinstance(item, str) for item in self.extracted_data):
            print("Simple string array detected")
            set_info_msgs(self, 'info', 'Simple string array detected')
            return process_contrats(self, self.extracted_data)
