from html.parser import HTMLParser


class CodeChefHTMLParser(HTMLParser):

    start = False
    sampleInput = ""
    sampleOutput = ""
    problemStatement = ""

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.start = True

    def handle_data(self, data):

        if self.start:
            data = self.formatData(data)
            self.problemStatement = self.problemStatement + '\n' + data

            if 'Example Input' in data:
                self.sampleInput = data.replace('Example Input', '')

            if 'Example Output' in data:
                self.sampleOutput = data.replace('Example Output', '')

    def formatData(self, data):

        # Removing ` as mdv can't render it
        data = data.replace('`', '')

        # Parsing Latex, unefficient way
        # Replace with more efficient and logically correct way
        data = data.replace('\dots', '...')
        data = data.replace('\le', '<=')
        data = data.replace('\ge', '>=')
        data = data.replace('_', '')
        data = data.replace('$', '*')

        return data

    def getProblemStatement(self):
        return self.problemStatement

    def getSampleInput(self):
        return self.sampleInput

    def getSampleOutput(self):
        return self.sampleOutput
