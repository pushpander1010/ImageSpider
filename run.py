import re
import subprocess
import os

def update_spider(website, follow):
    # Ensure the URL is correctly formatted
    if not re.match(r'^http[s]?://', website):
        website = "https://" + website
    
    # Read the existing spider file
    spider_file_path = "./ImageBot/ImageBot/spiders/spider.py"
    if not website=="https://":
        with open(spider_file_path, "r") as file:
            lines = file.readlines()
        
        # Update start_urls
        new_lines = []
        for line in lines:
            if re.match(r'.*start_urls.*', line):
                new_line = f'    start_urls = ["{website}"]\n'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        # Write the updated start_urls back to the spider file
        with open(spider_file_path, "w") as file:
            file.writelines(new_lines)
        
        print("The spider has been updated with the new website.")
    
    # Read the file again for the follow links update
    with open(spider_file_path, "r") as file:
        lines = file.readlines()
    
    # Update follow links
    new_lines = []
    flag=False
    for line in lines:
        if follow == False:
            if re.match(r'.*for page in response.css\("a::attr\(href\)"\).getall\(\):.*', line):
                continue
            elif re.match(r'.*response.follow.*', line):
                continue
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            flag=flag or re.match(r'.*for page in response.css\("a::attr\(href\)"\).getall\(\):.*', line)
    if follow==True and not flag:
        new_lines.append('\n')
        new_lines.append('        for page in response.css("a::attr(href)").getall():\n')
        new_lines.append('            yield response.follow(page, callback=self.parse)\n')
    
    # Write the updated follow links back to the spider file
    with open(spider_file_path, "w") as file:
        file.writelines(new_lines)
    
    print("The spider has been updated to follow links." if follow else "The spider has been updated not to follow links.")
    
    # Run the Scrapy spider
    result = subprocess.run(
        ["scrapy", "crawl", "spider", "-O", "data.json"],
        cwd=os.path.abspath("./ImageBot"),  # Set the working directory
        capture_output=True,
        text=True
    )
    
    # Print the output and errors (if any)
    print("Output:")
    print(result.stdout)
    print("Errors:")
    print(result.stderr)

if __name__ == "__main__":
    website = input("Enter the URL you want to get images from: ")
    follow = input("Do you want the spider to crawl to other pages? (yes/no): ").strip().lower() == 'yes'
    update_spider(website, follow)
