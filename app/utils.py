import datetime
import dateutil.parser as dparser


class ImageExtractor():
    image_str: str = ''
    steps: float = 0.0
    tracked_on: datetime.date = datetime.date.today()

    def __init__(self, image_str: str = ''):
        self.image_str = image_str
        self._extract()

    def _extract(self):
        self._extract_steps()
        self._extract_date()

    def _extract_steps(self):
        self.image_str = self.image_str.lower()
        if 'steps' in self.image_str:
            for line in self.image_str.splitlines():
                if 'steps' in line:
                    interim = line.split('steps')[0].split(' ')
                    try:
                        self.steps = float(interim[0].strip())
                        break
                    except:
                        pass

    def _extract_date(self):
        for line in self.image_str.splitlines():
            try:
                self.tracked_on = dparser.parse(line, fuzzy=True)
                break
            except:
                pass
