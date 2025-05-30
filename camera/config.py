import toml
import os
import weompy
import numpy as np
import re


class Config:
    def __init__(self, coreManager: weompy.CoreManager, path=None):
        self._path = (
            os.path.join(os.curdir, self._get_filename())
            if path == None
            else os.path.join(path, self._get_filename())
        )
        self._core = coreManager

    def write(self):
        config = toml.load(self._path)["properties"]
        self._try_connection()
        for property in config:
            if (
                property == "UART_BAUDRATE_CURRENT"
                or property == "UART_BAUDRATE_IN_FLASH"
            ):
                tmp = config[property]
                match = re.search(r"^<(.+)\x2E(.+): (.+)>$", tmp)
                if match == None:
                    continue

                cls = getattr(weompy, match.group(1))
                con = getattr(cls, match.group(2))
                prop = getattr(weompy, match.group(2))

                # tmp = weompy.Baudrate.B_3000000
                self._core.setPropertyValue(property, con.value)
        self._core.disconnect()

    def _get_filename(self):
        return os.path.join("camera", "config.toml")

    def _is_current(self, str) -> bool:
        return True if re.match("^.*_CURRENT$", str) != None else False

    def _is_in_flash(self, str) -> bool:
        return True if re.match("^.*_IN_FLASH$", str) != None else False

    def _is_standalone(self, str) -> bool:
        if self._is_current(str) or self._is_in_flash(str):
            return False
        else:
            return True

    def _try_connection(self):
        try:
            self._core.connectUartAuto()
        except Exception as e:
            print(e)

    def save(self):
        self._try_connection()
        properties = np.array(self._core.getPropertyIds())
        mask = [self._core.isPropertyWritable(p) for p in properties]
        writeables = properties[mask]
        config = dict()
        config["properties"] = dict()
        for i, writeable in enumerate(writeables):
            if self._is_standalone(writeable):
                config["properties"][
                    f"#{i} {self._core.getPropertyDescription(writeable)}"
                ] = "#"
                config["properties"][writeable] = self._core.getPropertyValue(writeable)
                continue
            if self._is_current(writeable):
                config["properties"][
                    f"#{i} {self._core.getPropertyDescription(writeable)}"
                ] = "#"
                config["properties"][writeable] = self._core.getPropertyValue(writeable)
                prop = writeable.replace("_CURRENT", "_IN_FLASH")
                config["properties"][prop] = self._core.getPropertyValue(prop)

        with open(self._path, "w") as f:
            toml_strings = toml.dumps(config).split("\n")
            pattern = r'^"(#){0,1}(?:\d+ ){0,1}(.+)(" = "#")$'
            repl = r"\1 \2"
            for s in toml_strings:
                if len(s) == 0:
                    continue
                line = re.sub(pattern=pattern, repl=repl, string=s)
                line = f"{line}\n"
                if line[0] == "#":
                    line = f"\n{line}"
                f.write(line)
            f.close()
        self._core.disconnect()


if __name__ == "__main__":
    core1 = weompy.CoreManager()
    try:
        config = Config(core1)
        config.write()
    except Exception as e:
        print(e)
    core1.disconnect()
