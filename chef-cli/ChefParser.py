from html.parser import HTMLParser


class CodeChefHTMLParser(HTMLParser):

    sampleInput = ""
    sampleOutput = ""
    problemStatement = ""
    space = ""
    isATagContent = False
    isHTagContent = False

    def handle_starttag(self, tag, attrs):

        tag = tag.lower()

        # Convert HTML tag to markdown for easy rendering by mdv
        if tag == 'h1':
            self.problemStatement += '# '
            self.isHTagContent = True
        elif tag == 'h2':
            self.problemStatement += '## '
            self.isHTagContent = True
        elif tag == 'h3':
            self.problemStatement += '### '
            self.isHTagContent = True
        elif tag == 'h4':
            self.problemStatement += '#### '
            self.isHTagContent = True
        elif tag == 'h5':
            self.problemStatement += '##### '
            self.isHTagContent = True
        elif tag == 'h6':
            self.problemStatement += '###### '
            self.isHTagContent = True
        elif tag == 'b':
            self.problemStatement += '**'
        elif tag == 'i':
            self.problemStatement += '*'
        elif tag == 'ol' or tag == 'ul':
            self.problemStatement += '\n'
            self.space += " "
        elif tag == 'li':
            self.problemStatement = self.problemStatement + self.space + "- "
        elif tag == 'p':
            self.problemStatement += '\n'
        elif tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.problemStatement = self.problemStatement + \
                        '[{0}](' + attr[1] + ')'
                    self.isATagContent = True

    def handle_endtag(self, tag):

        tag = tag.lower()

        if tag == 'b':
            self.problemStatement += '**'
        elif tag == 'i':
            self.problemStatement += '*'
        elif tag == 'ol' or tag == 'ul':
            self.space = self.space[:-1]
            self.problemStatement += '\n'
        elif tag == 'li':
            self.problemStatement += '\n'
        elif tag == 'a':
            self.isATagContent = False
        elif ((tag == 'br' or tag == 'hr') and not self.isATagContent and not self.isHTagContent):
            self.problemStatement += '\n'
        elif tag == 'h1' or tag == 'h2' or tag == 'h3' or tag == 'h4' or tag == 'h5' or tag == 'h6':
            self.problemStatement += '\n'
            self.isHTagContent = False

    def handle_data(self, data):

        data = self.formatData(data)
        if self.isATagContent:
            self.problemStatement = self.problemStatement.format(data)
        else:
            # self.problemStatement = self.problemStatement + '\n' + data
            self.problemStatement += data

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
        data = data.replace('\lt', '<')
        data = data.replace('\gt', '>')
        data = data.replace('_', '')
        data = data.replace('$', '*')

        return data

    def getProblemStatement(self):
        return self.problemStatement

    def getSampleInput(self):
        return self.sampleInput

    def getSampleOutput(self):
        return self.sampleOutput
